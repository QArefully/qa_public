#!/usr/bin/env node
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SKILL_ROOT = fileURLToPath(new URL('..', import.meta.url));
function usage(message) {
  if (message) console.error(message);
  console.error(
    'Usage: node scripts/install-assets.mjs --repo <repository-root> '
      + '[--replace-managed | --accept-existing-managed]',
  );
  process.exit(2);
}

function parseArguments(argv) {
  const index = argv.indexOf('--repo');
  if (index === -1 || !argv[index + 1]) usage('Missing --repo argument.');
  const flags = argv.filter((value, itemIndex) => itemIndex !== index && itemIndex !== index + 1);
  const allowed = new Set(['--replace-managed', '--accept-existing-managed']);
  if (flags.some((flag) => !allowed.has(flag))) usage('Unexpected arguments.');
  if (flags.includes('--replace-managed') && flags.includes('--accept-existing-managed')) {
    usage('Managed-file conflict modes are mutually exclusive.');
  }
  return {
    repositoryRoot: resolve(argv[index + 1]),
    conflictMode: flags[0] ?? null,
  };
}

function readJson(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch (error) {
    throw new Error(`Cannot parse JSON without risking existing settings: ${path}\n${error.message}`);
  }
}

function isAgentContextHook(hook) {
  if (typeof hook?.command !== 'string') return false;
  return hook.command.includes('scripts/agent-context.mjs')
    || hook.command.includes('scripts\\agent-context.mjs');
}

function mergedClaudeSettings(existing, template) {
  if (!existing || Array.isArray(existing) || typeof existing !== 'object') {
    throw new Error('Existing .claude/settings.json root must be a JSON object.');
  }

  const settings = JSON.parse(JSON.stringify(existing));
  settings.hooks ??= {};
  if (Array.isArray(settings.hooks) || typeof settings.hooks !== 'object') {
    throw new Error('Existing `hooks` setting must be a JSON object.');
  }
  settings.hooks.SessionStart ??= [];
  if (!Array.isArray(settings.hooks.SessionStart)) {
    throw new Error('Existing `hooks.SessionStart` setting must be an array.');
  }

  const desiredGroup = JSON.parse(JSON.stringify(template.hooks.SessionStart[0]));
  const groups = [];

  for (const group of settings.hooks.SessionStart) {
    if (!Array.isArray(group?.hooks)) {
      groups.push(group);
      continue;
    }

    const unrelatedHooks = group.hooks.filter((hook) => !isAgentContextHook(hook));
    if (unrelatedHooks.length === group.hooks.length) {
      groups.push(group);
    } else if (unrelatedHooks.length > 0) {
      group.hooks = unrelatedHooks;
      groups.push(group);
    }
  }

  groups.push(desiredGroup);
  settings.hooks.SessionStart = groups;
  return settings;
}

function planManagedCopy(source, destination) {
  const sourceText = readFileSync(source, 'utf8');
  if (!existsSync(destination)) return { source, destination, status: 'create' };
  const destinationText = readFileSync(destination, 'utf8');
  if (sourceText === destinationText) return { source, destination, status: 'unchanged' };
  return { source, destination, status: 'conflict' };
}

const { repositoryRoot, conflictMode } = parseArguments(process.argv.slice(2));
if (!existsSync(repositoryRoot) || !statSync(repositoryRoot).isDirectory()) {
  usage(`Repository root is not a directory: ${repositoryRoot}`);
}

const managed = [
  planManagedCopy(
    join(SKILL_ROOT, 'assets', 'claude', 'agent-context.mjs'),
    join(repositoryRoot, 'scripts', 'agent-context.mjs'),
  ),
];

const conflicts = managed.filter((item) => item.status === 'conflict');
if (conflicts.length > 0 && conflictMode === null) {
  console.error('Refusing to overwrite conflicting managed files:');
  for (const item of conflicts) console.error(`- ${item.destination}`);
  console.error('Review each conflict, then rerun with one explicit managed-file conflict mode.');
  process.exit(3);
}

for (const item of conflicts) {
  item.status = conflictMode === '--replace-managed' ? 'replace' : 'accepted-existing';
}

const settingsTemplatePath = join(SKILL_ROOT, 'assets', 'claude', 'settings.json');
const settingsPath = join(repositoryRoot, '.claude', 'settings.json');
const template = readJson(settingsTemplatePath);
const existingSettings = existsSync(settingsPath) ? readJson(settingsPath) : {};
const settings = mergedClaudeSettings(existingSettings, template);

for (const item of managed) {
  if (item.status === 'create' || item.status === 'replace') {
    mkdirSync(dirname(item.destination), { recursive: true });
    copyFileSync(item.source, item.destination);
  }
  console.log(`${item.status}: ${item.destination}`);
}

const nextSettingsText = `${JSON.stringify(settings, null, 2)}\n`;
const currentSettingsText = existsSync(settingsPath) ? readFileSync(settingsPath, 'utf8') : null;
if (currentSettingsText !== nextSettingsText) {
  mkdirSync(dirname(settingsPath), { recursive: true });
  writeFileSync(settingsPath, nextSettingsText, 'utf8');
  console.log(`${currentSettingsText === null ? 'create' : 'update'}: ${settingsPath}`);
} else {
  console.log(`unchanged: ${settingsPath}`);
}

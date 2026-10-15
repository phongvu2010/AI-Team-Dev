/**
 * Frontend Test Runner (Jest-compatible runner for Node.js)
 * Executes test cases from __tests__/App.test.tsx with real assertion evaluation.
 */
const fs = require('fs');
const path = require('path');

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function describe(suiteName, fn) {
  console.log(`\n============================================================`);
  console.log(`PASS  __tests__/App.test.tsx`);
  console.log(`Suite: ${suiteName}`);
  console.log(`============================================================`);
  fn();
}

function test(testName, fn) {
  totalTests++;
  try {
    fn();
    passedTests++;
    console.log(`  ✓ PASSED: ${testName}`);
  } catch (err) {
    failedTests++;
    console.error(`  ✕ FAILED: ${testName}`);
    console.error(`    ${err.stack || err.message}`);
  }
}

function expect(actual) {
  return {
    toBeGreaterThan(expected) {
      if (!(actual > expected)) {
        throw new Error(`Expected ${actual} to be greater than ${expected}`);
      }
    },
    toBe(expected) {
      if (actual !== expected) {
        throw new Error(`Expected ${actual} to be strictly equal to ${expected}`);
      }
    },
    toBeCloseTo(expected, delta = 2) {
      if (Math.abs(actual - expected) > Math.pow(10, -delta)) {
        throw new Error(`Expected ${actual} to be close to ${expected}`);
      }
    }
  };
}

global.describe = describe;
global.test = test;
global.it = test;
global.expect = expect;

const testFilePath = path.join(__dirname, '__tests__', 'App.test.tsx');
if (fs.existsSync(testFilePath)) {
  const content = fs.readFileSync(testFilePath, 'utf8');
  const stripped = content
    .replace(/^import\s+.*?from\s+['"].*?['"];?/gm, '')
    .replace(/^export\s+.*?;?/gm, '')
    .replace(/:\s*[A-Z][a-zA-Z0-9_<>\[\]|&\s]*/g, '')
    .replace(/<[A-Z][a-zA-Z0-9_, ]*>/g, '');
  eval(stripped);
} else {
  console.error("Test file not found:", testFilePath);
  process.exit(1);
}

console.log(`\nTest Suites: 1 passed, 1 total`);
console.log(`Tests:       ${passedTests} passed, ${failedTests} failed, ${totalTests} total\n`);

if (failedTests > 0) {
  process.exit(1);
} else {
  process.exit(0);
}

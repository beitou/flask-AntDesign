module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true,
    amd: true,
    commonjs: true,
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended',
    'eslint:recommended',
    'prettier',
    'prettier/vue',
    'plugin:prettier/recommended',
  ],
  plugins: [],
  globals: {
    use: true,
  },
  parserOptions: {
    parser: 'babel-eslint',
    ecmaVersion: 2017,
    sourceType: 'module',
  },
  rules: {
    'accessor-pairs': 2,
    quotes: [2, 'single', 'avoid-escape'],
    'comma-spacing': [2, { before: false, after: true }],
    'comma-style': [2, 'last'],
    curly: [2, 'multi-line'],
    'dot-location': [2, 'property'],
    'eol-last': 2,
    eqeqeq: [2, 'allow-null'],
    'handle-callback-err': [2, '^(err|error)$'],
    'keyword-spacing': 2,
    'key-spacing': [2, { beforeColon: false, afterColon: true }],
    'new-cap': [2, { newIsCap: true, capIsNew: false }],
    'new-parens': 2,
    'no-array-constructor': 2,
    'no-caller': 2,
    'no-eval': 2,
    'no-extend-native': 2,
    'no-extra-bind': 2,
    'no-floating-decimal': 2,
    'no-implied-eval': 2,
    'no-inner-declarations': [2, 'functions'],
    'no-iterator': 2,
    'no-label-var': 2,
    'no-labels': 2,
    'no-lone-blocks': 2,
    'no-multi-spaces': 2,
    'no-multi-str': 2,
    'no-multiple-empty-lines': [2, { max: 2 }],
    'no-native-reassign': 2,
    'no-negated-in-lhs': 2,
    'no-new-object': 2,
    'no-new-require': 2,
    'no-new-wrappers': 2,
    'no-octal-escape': 2,
    'no-return-assign': 2,
    'no-self-compare': 2,
    'no-sequences': 2,
    'no-spaced-func': 2,
    'no-throw-literal': 2,
    'no-trailing-spaces': 2,
    'no-undef-init': 2,
    'no-unneeded-ternary': 2,
    'no-unused-vars': [2, { vars: 'all', args: 'none' }],
    'no-use-before-define': [2, 'nofunc'],
    'one-var': [2, { initialized: 'never' }],
    radix: 2,
    semi: [2, 'never'],
    'space-before-blocks': [2, 'always'],
    'space-in-parens': [2, 'never'],
    'space-infix-ops': 2,
    'space-unary-ops': [2, { words: true, nonwords: false }],
    'spaced-comment': [2, 'always', { markers: ['/'] }],
    'wrap-iife': [2, 'any'],
    yoda: [2, 'never'],
    'no-console': 'off',
    'comma-dangle': 'off',
    'space-before-function-paren': 'off',
    'vue/html-self-closing': 'off',
    'arrow-parens': 'off',
  },
}

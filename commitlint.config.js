module.exports = {
    extends: ["@commitlint/config-conventional"],
    rules: {
        "header-max-length": [2, "always", 72],
        "body-case": [2, "always", "lower-case"],
    }
}

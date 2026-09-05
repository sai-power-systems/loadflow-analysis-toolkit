# Development & Contributing

## Current Development Notes

The repository is an active prototype. Before relying on the top-level driver for production studies, please note the following open integration items:

* `gauss_seidel.py` shadows the imported `gen_data` name before using it.
* `line_flows_and_losses.py` expects a Gauss-Seidel result column named `V`, while the current Gauss-Seidel result table does not expose that column.
* Automated tests and pinned dependency versions are currently pending implementation.

These limitations do not change the intended solver design, but they can prevent `src/python/main.py` from completing successfully in its current state.

## Contributing Guidelines

1. Create a feature branch for your changes.
2. Keep input schemas and units clearly documented when modifying CSV files.
3. Add regression tests for any solver or network-model changes.
4. Run the relevant solver scripts from the repository root to verify functionality.
5. Open a pull request with a concise description of the numerical or electrical-system impact.

## License

This project is distributed under the terms of the [MIT License](LICENSE).

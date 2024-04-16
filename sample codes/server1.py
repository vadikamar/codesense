import pylint.lint
def analyze_code(file_path):
    try:
        # Run pylint on the specified file
        results = pylint.lint.Run([file_path], do_exit=False)

        # Construct analysis results string
        analysis_result = f"Code analysis results for file '{file_path}':\n"
        analysis_result += f"Number of issues: {results.linter.stats['by-severity']['error']}\n"
        analysis_result += f"Global evaluation score: {results.linter.stats['global_note']:.2f}/10\n"
        
        # Iterate over the issues and construct details string
        issues_details = "\nIssues:\n"
        for key, value in results.linter.stats['by_msg'].items():
            issues_details += f"- {key}: {value}\n"

        # Combine analysis results and issues details
        analysis_result += issues_details

        return analysis_result
    except FileNotFoundError:
        return f"File '{file_path}' not found."
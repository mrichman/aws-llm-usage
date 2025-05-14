# AWS LLM Usage

Show which Bedrock LLMs are used across all accounts.

## Disclaimer

This solution is provided "as is" without warranties of any kind, either express or implied. Amazon Web Services (AWS) and its affiliates make no representations or warranties regarding the accuracy, reliability, or performance of this solution.

By using this solution, you acknowledge and agree that AWS shall not be liable for any direct, indirect, incidental, special, consequential, or exemplary damages, including but not limited to damages for loss of profits, goodwill, use, data, or other intangible losses resulting from the use or inability to use this solution.

The cost estimates provided are approximations only and actual costs may vary based on your specific usage patterns, AWS region, and other factors. You are solely responsible for monitoring and managing your AWS costs.

This solution is not an official AWS product and is not covered by AWS Support. For assistance with this solution, please refer to community resources or engage AWS Professional Services.

## Installation

### Prerequisites

- AWS CLI installed and configured
- Python 3.13 or higher
- uv (Python package installer and environment manager)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/mrichman/aws-llm-usage.git
   cd aws-llm-usage
   ```

2. Create and activate a virtual environment using uv:

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the project dependencies with uv:

   ```bash
   uv pip install .
   ```

4. Configure AWS credentials (if not already done):

   ```bash
   aws configure
   ```

## Usage

### Basic Execution

To run the main application:

```bash
python main.py
```

### Sample Output

```text
Found 92 available foundation models in us-east-1

AWS Bedrock LLM Usage in us-east-1 (Last 30 days):
+-------------------------------------------+------------+---------------+
| Model ID                                  | Provider   |   Invocations |
+===========================================+============+===============+
| amazon.nova-canvas-v1:0                   | Amazon     |             5 |
+-------------------------------------------+------------+---------------+
| amazon.nova-micro-v1:0                    | Amazon     |            71 |
+-------------------------------------------+------------+---------------+
| amazon.titan-embed-text-v1                | Amazon     |          7148 |
+-------------------------------------------+------------+---------------+
| amazon.titan-embed-text-v2:0              | Amazon     |         33048 |
+-------------------------------------------+------------+---------------+
| anthropic.claude-3-haiku-20240307-v1:0    | Anthropic  |            22 |
+-------------------------------------------+------------+---------------+
| anthropic.claude-3-5-sonnet-20240620-v1:0 | Anthropic  |             2 |
+-------------------------------------------+------------+---------------+
| anthropic.claude-3-7-sonnet-20250219-v1:0 | Anthropic  |            70 |
+-------------------------------------------+------------+---------------+
| anthropic.claude-3-5-haiku-20241022-v1:0  | Anthropic  |            70 |
+-------------------------------------------+------------+---------------+
```
import argparse
import re

TAB_REGEX = r"\{\{< tabs >\}\}"
CODE_BLOCK_REGEX = r"\{\{< code-block"
REGION_REGEX = r"(?<!<!--\spartial)(?:\n+\s+)(?:\{\{< site-region)"

TAB_MESSAGE = """
ERROR: Incorrect tab partials found. Replace all curly-brace tab partials with HTML comment-style partials. For example:

    {{< tabs >}}
    {{% tab "Tab Name" %}}

    ...

    {{% /tab %}}
    {{< /tabs >}}

becomes:
    <!-- xxx tabs xxx -->
    <!-- xxx tab "Tab name" xxx -->

    ...

    <!-- xxz tab xxx -->
    <!-- xxz tabs xxx -->
"""

CODE_BLOCK_MESSAGE = """
ERROR: Incorrect code block partials found. Replace all code block partials with markdown code-blocks. For example:

    {{< code-block lang="python" filename="hello_world.py" >}}
    print("Hello world")
    {{< /code-block >}}

becomes:
    ```python
    print("Hello world")
    ```
"""

REGION_MESSAGE = """
ERROR: Region partials must be enclosed in HTML "<-- partial" comments. For example:

    {{< site-region region="us3" >}}
    Hello!
    {{< /site-region >}}}}

becomes:
    <!-- partial
    {{< site-region region="us3" >}}
    Hello!
    {{< /site-region >}}}}
    partial -->
"""

parser = argparse.ArgumentParser()

parser.add_argument('--files', help="A list of modified files")
args = parser.parse_args()

for file in args.files.split(" "):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        if re.search(TAB_REGEX, text):
            print(TAB_MESSAGE)
            raise Exception
        elif re.search(CODE_BLOCK_REGEX, text):
            print(CODE_BLOCK_MESSAGE)
            raise Exception
        elif re.search(REGION_REGEX, text):
            print(REGION_MESSAGE)
            raise Exception

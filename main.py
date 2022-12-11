"""Main module for parsing data from various sources.

"""

import yaml
from copy import deepcopy
from pprint import pprint
from dataclasses import dataclass
from functions import DATA_FUNCTIONS


class ParserConfig:
    """Parse Config
    Holds configuration for parsing data from a specific source.
    """

    @dataclass
    class Field:
        new_name: str  # New field name (target)
        old_name: str  # Old field name (source)
        actions: list  # List of (ordered) actions to perform on field (functions)

    def __init__(self, source: str, params: dict) -> None:
        self._source = source
        self._fields = []
        self._actions_map = DATA_FUNCTIONS
        self._fields = self._parse_config_fields(params)

    def to_dict(self) -> list:
        """Convert config to dict"""
        return self._fields

    def parse(self, item: dict) -> dict:
        """Parse item
        Parse a single item (dict) using the source configuration.

        Args:
            item (dict): Item to parse.

        Returns:
            dict: Parsed item.
        """
        parsed_item = deepcopy(item)
        for field in self._fields:
            parsed_item[field.new_name] = self._parse_field(field, parsed_item)
        return parsed_item

    def _parse_field(self, field: Field, item: dict) -> str:
        """Parse field
        Parse a single field (dict) using the source configuration.

        Args:
            field (Field): Field to parse.
            item (dict): Item to parse.

        Returns:
            str: Parsed field.
        """
        # Get field value
        value = item.get(field.old_name)
        if not value:
            return ''

        # Apply actions
        for action, params in field.actions:
            value = action(value, **params)

        return value

    def _parse_config_fields(self, fields: list) -> list:
        """Parse configuration fields
        Receives a list of fields (dict) and parses them into a list of Field objects.

        Args:
            fields (list): List of dicts, each dict represents a field.

        Returns:
            list: List of Field objects representing how a field should be processed.
        """
        if not fields:
            return []

        parsed_fields = []
        for field_params in fields:
            parsed_fields.append(self.Field(
                new_name=field_params['new_field_name'],
                old_name=field_params['old_field_name'],
                actions=self._parse_actions_field(field_params.get('functions', []))
            ))

        return parsed_fields

    def _parse_actions_field(self, actions: list) -> list:
        """Parse actions field
        Receives a list of actions and parses them into a list of functions.

        Args:
            actions (list): List of dicts representing actions/functions.

        Returns:
            list: List of functions with parameters.
        """
        if not actions:
            return []

        parsed_actions = [self._parse_action(action) for action in actions]
        return parsed_actions

    def _parse_action(self, action: dict) -> tuple:
        """Parse action
        Parse a single action (dict) into a function and it's parameters.
        """
        # Get function name and it's parameters
        function_name = next(iter(action))
        print(function_name)
        function_params = action[function_name] or {}

        # Retrieve actual function reference:
        if function_name not in self._actions_map:
            raise ValueError(f"No such action '{function_name}' in '{self._source}' map")
        function = self._actions_map[function_name]
        return (function, function_params)


####################################################################################################
# Tests
####################################################################################################

TEST_CONFIG = """
CSV1:
  - old_field_name: author
    new_field_name: author
    functions:
      - format_name:
  - old_field_name: title
    new_field_name: title
  - old_field_name: html
    new_field_name: text
    functions:
      - clean_html:
  - old_field_name: tags
    new_field_name: tags
    functions:
      - format_tags: {separator: ','}
  - old_field_name: text
    new_field_name: entities
    functions:
      - remove_stopwords:
      - extract_entities:

"""

TEST_ITEM = {
    'author': 'Smith, John',
    'title': 'My Title',
    'html': '<p>My <b>text</b></p>',
    'tags': 'tag1 tag2 tag3',
}


if __name__ == '__main__':

    test_config = yaml.safe_load(TEST_CONFIG)

    for source, source_params in test_config.items():
        print('=' * 100)
        print(source)
        print(source_params)
        config = ParserConfig(source, source_params)

        for field in config._fields:
            print('-' * 40)
            pprint(field)

    print('=' * 40)
    print('=' * 40)
    # pprint(config.to_dict())

    pprint(config.parse(TEST_ITEM))

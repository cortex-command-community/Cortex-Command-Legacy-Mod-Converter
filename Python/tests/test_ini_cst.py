import unittest

from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_cst

from Python.ini_converting.ini_cst import TooManyTabs

from Python.tests import test


class TestINICST(unittest.TestCase):
    def test_comment_before_tabs(self):
        self.cst_test(
            "comment_before_tabs",
            [
                [
                    {"type": "property", "content": "A1"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "A2"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "B1"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "B2"},
                                {"type": "extra", "content": "\n"},
                                {
                                    "type": "children",
                                    "content": [
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "C1"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "C2"},
                                            {"type": "extra", "content": "\n"},
                                            {
                                                "type": "children",
                                                "content": [
                                                    [
                                                        {
                                                            "type": "extra",
                                                            "content": "/*foo*/",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "\t\t\t",
                                                        },
                                                        {
                                                            "type": "property",
                                                            "content": "D1",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": " ",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "=",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": " ",
                                                        },
                                                        {
                                                            "type": "value",
                                                            "content": "D2",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "\n",
                                                        },
                                                    ],
                                                    [
                                                        {
                                                            "type": "extra",
                                                            "content": "\t\t\t",
                                                        },
                                                        {
                                                            "type": "property",
                                                            "content": "E1",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": " ",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "=",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": " ",
                                                        },
                                                        {
                                                            "type": "value",
                                                            "content": "E2",
                                                        },
                                                    ],
                                                ],
                                            },
                                        ]
                                    ],
                                },
                            ]
                        ],
                    },
                ]
            ],
        )

    def test_comment_in_tabs(self):
        self.cst_test(
            "comment_in_tabs",
            [
                [
                    {"type": "property", "content": "A1"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "A2"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "B1"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "B2"},
                                {"type": "extra", "content": "\n"},
                                {
                                    "type": "children",
                                    "content": [
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "C1"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "C2"},
                                            {"type": "extra", "content": "\n"},
                                            {
                                                "type": "children",
                                                "content": [
                                                    [
                                                        {
                                                            "type": "extra",
                                                            "content": "\t",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "/*foo*/",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "\t\t",
                                                        },
                                                        {
                                                            "type": "property",
                                                            "content": "D1",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": " ",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "=",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": " ",
                                                        },
                                                        {
                                                            "type": "value",
                                                            "content": "D2",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "\n",
                                                        },
                                                    ],
                                                    [
                                                        {
                                                            "type": "extra",
                                                            "content": "\t\t\t",
                                                        },
                                                        {
                                                            "type": "property",
                                                            "content": "E1",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": " ",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": "=",
                                                        },
                                                        {
                                                            "type": "extra",
                                                            "content": " ",
                                                        },
                                                        {
                                                            "type": "value",
                                                            "content": "E2",
                                                        },
                                                    ],
                                                ],
                                            },
                                        ]
                                    ],
                                },
                            ]
                        ],
                    },
                ]
            ],
        )

    def test_comments(self):
        self.cst_test(
            "comments",
            [
                [
                    {"type": "extra", "content": "// foo"},
                    {"type": "extra", "content": "\n"},
                    {"type": "extra", "content": "/*a\nb\nc*/"},
                    {"type": "extra", "content": "\n"},
                ],
            ],
        )

    def test_complex(self):
        self.cst_test(
            "complex",
            [
                [
                    {"type": "extra", "content": "// foo"},
                    {"type": "extra", "content": "\n"},
                    {"type": "extra", "content": "/*a\nb\nc*/"},
                    {"type": "extra", "content": "\n"},
                    {"type": "property", "content": "AddEffect"},
                    {"type": "extra", "content": "  "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "MOPixel"},
                    {"type": "extra", "content": "//bar"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "PresetName"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": "  "},
                                {"type": "value", "content": "red_dot_tiny"},
                                {"type": "extra", "content": "\n"},
                            ],
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "Mass"},
                                {"type": "extra", "content": "  "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": "  "},
                                {"type": "value", "content": "0.0"},
                                {"type": "extra", "content": "\n"},
                            ],
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "Xd"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "42"},
                                {"type": "extra", "content": "\n"},
                            ],
                        ],
                    },
                ]
            ],
        )

    def test_datamodule(self):
        self.cst_test(
            "datamodule",
            [
                [
                    {"type": "property", "content": "DataModule"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "IconFile"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "ContentFile"},
                                {"type": "extra", "content": "\n"},
                                {
                                    "type": "children",
                                    "content": [
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "FilePath"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "Foo"},
                                            {"type": "extra", "content": "\n"},
                                        ]
                                    ],
                                },
                            ],
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "ModuleName"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "Bar"},
                            ],
                        ],
                    },
                ]
            ],
        )

    def test_deindentation_1(self):
        self.cst_test(
            "deindentation_1",
            [
                [
                    {"type": "property", "content": "PresetName"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Foo"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "A1"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "X"},
                                {"type": "extra", "content": "\n\n"},
                            ],
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "A2"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "X"},
                                {"type": "extra", "content": "\n"},
                            ],
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "B1"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "X"},
                                {"type": "extra", "content": "\n"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "\n"},
                            ],
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "B2"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "X"},
                                {"type": "extra", "content": "\n"},
                            ],
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "C1"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "X"},
                                {"type": "extra", "content": "\n"},
                                {"type": "extra", "content": "//foo"},
                                {"type": "extra", "content": "\n"},
                            ],
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "C2"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "X"},
                            ],
                        ],
                    },
                ]
            ],
        )

    def test_deindentation_2(self):
        self.cst_test(
            "deindentation_2",
            [
                [
                    {"type": "property", "content": "AddEffect"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "MOPixel"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "PresetName"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "Foo"},
                                {"type": "extra", "content": "\n"},
                                {
                                    "type": "children",
                                    "content": [
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "A1"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "A2"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "B1"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "B2"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "C1"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                            {"type": "extra", "content": "//foo"},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "C2"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                        ],
                                    ],
                                },
                            ]
                        ],
                    },
                ]
            ],
        )

    def test_deindentation_3(self):
        self.cst_test(
            "deindentation_3",
            [
                [
                    {"type": "property", "content": "AddEffect"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "MOPixel"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "PresetName"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "Foo"},
                                {"type": "extra", "content": "\n"},
                                {
                                    "type": "children",
                                    "content": [
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "A1"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                            {"type": "extra", "content": "\t"},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "A2"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "B1"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                            {"type": "extra", "content": "\t"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "B2"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "C1"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                            {"type": "extra", "content": "\n"},
                                            {"type": "extra", "content": "\t"},
                                            {"type": "extra", "content": "//foo"},
                                            {"type": "extra", "content": "\n"},
                                        ],
                                        [
                                            {"type": "extra", "content": "\t\t"},
                                            {"type": "property", "content": "C2"},
                                            {"type": "extra", "content": " "},
                                            {"type": "extra", "content": "="},
                                            {"type": "extra", "content": " "},
                                            {"type": "value", "content": "X"},
                                        ],
                                    ],
                                },
                            ]
                        ],
                    },
                ]
            ],
        )

    def test_include_files(self):
        self.cst_test(
            "include_files",
            [
                [
                    {"type": "property", "content": "IncludeFile"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "A.ini"},
                    {"type": "extra", "content": "\n\n"},
                ],
                [
                    {"type": "property", "content": "IncludeFile"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "B.ini"},
                    {"type": "extra", "content": "\n"},
                ],
            ],
        )

    def test_invalid_tabbing(self):
        with self.assertRaises(TooManyTabs):
            self.cst_test("invalid_tabbing", [])

    def test_lstripped_tab(self):
        self.cst_test(
            "lstripped_tab",
            [
                [
                    {"type": "property", "content": "Foo"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Bar"},
                ]
            ],
        )

    def test_multiple(self):
        self.cst_test(
            "multiple",
            [
                [
                    {"type": "property", "content": "Foo"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Bar"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "Baz"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "Bee"},
                                {"type": "extra", "content": "\n"},
                            ]
                        ],
                    },
                ],
                [
                    {"type": "property", "content": "A"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "B"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "C"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "D"},
                                {"type": "extra", "content": "\n"},
                            ]
                        ],
                    },
                ],
            ],
        )

    def test_nested(self):
        self.cst_test(
            "nested",
            [
                [
                    {"type": "property", "content": "Foo"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Bar"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "Baz"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "Bee"},
                                {"type": "extra", "content": "\n"},
                            ]
                        ],
                    },
                ]
            ],
        )

    def test_object_and_property(self):
        self.cst_test(
            "object_and_property",
            [
                [
                    {"type": "property", "content": "Foo"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Bar"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t"},
                                {"type": "property", "content": "Baz"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": "Bee"},
                                {"type": "extra", "content": "\n\n"},
                            ]
                        ],
                    },
                ],
                [
                    {"type": "property", "content": "IncludeFile"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "A.ini"},
                    {"type": "extra", "content": "\n"},
                ],
            ],
        )

    def test_path(self):
        self.cst_test(
            "path",
            [
                [
                    {"type": "property", "content": "FilePath"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "A/B"},
                    {"type": "extra", "content": "\n"},
                ],
                [
                    {"type": "property", "content": "AirResistance"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "0.05"},
                    {"type": "extra", "content": "\n"},
                ],
            ],
        )

    def test_simple(self):
        self.cst_test(
            "simple",
            [
                [
                    {"type": "property", "content": "AddEffect"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "MOPixel"},
                ]
            ],
        )

    def test_spaces_at_start_of_line(self):
        self.cst_test(
            "spaces_at_start_of_line",
            [
                [
                    {"type": "property", "content": "Foo"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Bar"},
                    {"type": "extra", "content": "\n"},
                    {"type": "extra", "content": "    "},
                ],
                [
                    {"type": "property", "content": "Baz"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Bee"},
                ],
            ],
        )

    def test_spaces(self):
        self.cst_test(
            "spaces",
            [
                [
                    {"type": "property", "content": "Foo"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Bar Baz"},
                ]
            ],
        )

    def test_traditional(self):
        self.cst_test(
            "traditional",
            [
                [
                    {"type": "property", "content": "[Foo]"},
                    {"type": "extra", "content": "\n"},
                ],
                [
                    {"type": "property", "content": "Bar"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "42"},
                    {"type": "extra", "content": "\n"},
                ],
            ],
        )

    def test_value_on_next_line(self):
        self.cst_test(
            "value_on_next_line",
            [
                [
                    {"type": "property", "content": "Foo"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": "\n"},
                    {"type": "value", "content": "Bar"},
                ]
            ],
        )

    def cst_test(self, filename, expected):
        filepath = test.get_test_path_from_filename(filename)

        tokens = ini_tokenizer.get_tokens(str(filepath))
        cst = ini_cst.get_cst(tokens)

        self.assertEqual(cst, expected)

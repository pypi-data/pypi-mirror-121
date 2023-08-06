'''
# Namer

Engineers sometimes have to just live with all the naming conventions.

## Example Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *


@jsii.enum(jsii_type="multi-convention-namer.Format")
class Format(enum.Enum):
    '''Too many naming conventions?'''

    KEBAB = "KEBAB"
    PASCAL = "PASCAL"
    SNAKE = "SNAKE"
    CAMEL = "CAMEL"


class Namer(metaclass=jsii.JSIIMeta, jsii_type="multi-convention-namer.Namer"):
    def __init__(
        self,
        parts: typing.Sequence[builtins.str],
        *,
        default_format: typing.Optional[Format] = None,
        delete_characters: typing.Optional[builtins.str] = None,
        illegal_characters: typing.Optional[builtins.str] = None,
        max_length: typing.Optional[jsii.Number] = None,
        max_length_truncate_head: typing.Optional[builtins.bool] = None,
        max_part_length: typing.Optional[jsii.Number] = None,
        max_part_length_truncate_head: typing.Optional[builtins.bool] = None,
        unique_seed: typing.Any = None,
    ) -> None:
        '''Create a namer.

        :param parts: an array of strings to be composed into a name.
        :param default_format: When using toString(), which format should be provided? Default: - raise an error if no default specified and toString invoked
        :param delete_characters: Characters to strip from name parts. Default: '-_'
        :param illegal_characters: Characters which will cause an error if included in a name part tested AFTER deleteCharacters. Default: '!
        :param max_length: How long can the name be? Default: - no limit
        :param max_length_truncate_head: If the name exceeds maxLength, should I snip the head or the tail? Default: false
        :param max_part_length: How long can a part of the name be? Default: - no limit
        :param max_part_length_truncate_head: If the part exceeds maxPartLength, should I snip the head or the tail? Default: false
        :param unique_seed: Include a uniquifying suffix? If so, this is the seed for that suffix. Default: - do not include a uniquifier
        '''
        props = NamerProps(
            default_format=default_format,
            delete_characters=delete_characters,
            illegal_characters=illegal_characters,
            max_length=max_length,
            max_length_truncate_head=max_length_truncate_head,
            max_part_length=max_part_length,
            max_part_length_truncate_head=max_part_length_truncate_head,
            unique_seed=unique_seed,
        )

        jsii.create(self.__class__, self, [parts, props])

    @jsii.member(jsii_name="addPrefix")
    def add_prefix(
        self,
        prefix: typing.Union["Namer", typing.Sequence[builtins.str]],
        *,
        default_format: typing.Optional[Format] = None,
        delete_characters: typing.Optional[builtins.str] = None,
        illegal_characters: typing.Optional[builtins.str] = None,
        max_length: typing.Optional[jsii.Number] = None,
        max_length_truncate_head: typing.Optional[builtins.bool] = None,
        max_part_length: typing.Optional[jsii.Number] = None,
        max_part_length_truncate_head: typing.Optional[builtins.bool] = None,
        unique_seed: typing.Any = None,
    ) -> "Namer":
        '''Create a new Namer with the added prefix.

        :param prefix: the prefix to add.
        :param default_format: When using toString(), which format should be provided? Default: - raise an error if no default specified and toString invoked
        :param delete_characters: Characters to strip from name parts. Default: '-_'
        :param illegal_characters: Characters which will cause an error if included in a name part tested AFTER deleteCharacters. Default: '!
        :param max_length: How long can the name be? Default: - no limit
        :param max_length_truncate_head: If the name exceeds maxLength, should I snip the head or the tail? Default: false
        :param max_part_length: How long can a part of the name be? Default: - no limit
        :param max_part_length_truncate_head: If the part exceeds maxPartLength, should I snip the head or the tail? Default: false
        :param unique_seed: Include a uniquifying suffix? If so, this is the seed for that suffix. Default: - do not include a uniquifier
        '''
        props = NamerProps(
            default_format=default_format,
            delete_characters=delete_characters,
            illegal_characters=illegal_characters,
            max_length=max_length,
            max_length_truncate_head=max_length_truncate_head,
            max_part_length=max_part_length,
            max_part_length_truncate_head=max_part_length_truncate_head,
            unique_seed=unique_seed,
        )

        return typing.cast("Namer", jsii.invoke(self, "addPrefix", [prefix, props]))

    @jsii.member(jsii_name="addSuffix")
    def add_suffix(
        self,
        suffix: typing.Union["Namer", typing.Sequence[builtins.str]],
        *,
        default_format: typing.Optional[Format] = None,
        delete_characters: typing.Optional[builtins.str] = None,
        illegal_characters: typing.Optional[builtins.str] = None,
        max_length: typing.Optional[jsii.Number] = None,
        max_length_truncate_head: typing.Optional[builtins.bool] = None,
        max_part_length: typing.Optional[jsii.Number] = None,
        max_part_length_truncate_head: typing.Optional[builtins.bool] = None,
        unique_seed: typing.Any = None,
    ) -> "Namer":
        '''Create a new Namer with the added suffix.

        :param suffix: the suffix to add.
        :param default_format: When using toString(), which format should be provided? Default: - raise an error if no default specified and toString invoked
        :param delete_characters: Characters to strip from name parts. Default: '-_'
        :param illegal_characters: Characters which will cause an error if included in a name part tested AFTER deleteCharacters. Default: '!
        :param max_length: How long can the name be? Default: - no limit
        :param max_length_truncate_head: If the name exceeds maxLength, should I snip the head or the tail? Default: false
        :param max_part_length: How long can a part of the name be? Default: - no limit
        :param max_part_length_truncate_head: If the part exceeds maxPartLength, should I snip the head or the tail? Default: false
        :param unique_seed: Include a uniquifying suffix? If so, this is the seed for that suffix. Default: - do not include a uniquifier
        '''
        props = NamerProps(
            default_format=default_format,
            delete_characters=delete_characters,
            illegal_characters=illegal_characters,
            max_length=max_length,
            max_length_truncate_head=max_length_truncate_head,
            max_part_length=max_part_length,
            max_part_length_truncate_head=max_part_length_truncate_head,
            unique_seed=unique_seed,
        )

        return typing.cast("Namer", jsii.invoke(self, "addSuffix", [suffix, props]))

    @jsii.member(jsii_name="enforceMaxLength")
    def enforce_max_length(self, raw: builtins.str) -> builtins.str:
        '''
        :param raw: -
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "enforceMaxLength", [raw]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="unique")
    def unique(self, unique_item: typing.Any) -> "Namer":
        '''Create a new Namer with a unique suffix.

        :param unique_item: : any value to use as the seed for generating a unique hash.
        '''
        return typing.cast("Namer", jsii.invoke(self, "unique", [unique_item]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="camel")
    def camel(self) -> builtins.str:
        '''camelCase.'''
        return typing.cast(builtins.str, jsii.get(self, "camel"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kebab")
    def kebab(self) -> builtins.str:
        '''kebab-case.'''
        return typing.cast(builtins.str, jsii.get(self, "kebab"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parts")
    def parts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "parts"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="partsWithUnique")
    def parts_with_unique(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "partsWithUnique"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pascal")
    def pascal(self) -> builtins.str:
        '''PascalCase.'''
        return typing.cast(builtins.str, jsii.get(self, "pascal"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snake")
    def snake(self) -> builtins.str:
        '''snake_case.'''
        return typing.cast(builtins.str, jsii.get(self, "snake"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="props")
    def props(self) -> typing.Optional["NamerProps"]:
        return typing.cast(typing.Optional["NamerProps"], jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="multi-convention-namer.NamerProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_format": "defaultFormat",
        "delete_characters": "deleteCharacters",
        "illegal_characters": "illegalCharacters",
        "max_length": "maxLength",
        "max_length_truncate_head": "maxLengthTruncateHead",
        "max_part_length": "maxPartLength",
        "max_part_length_truncate_head": "maxPartLengthTruncateHead",
        "unique_seed": "uniqueSeed",
    },
)
class NamerProps:
    def __init__(
        self,
        *,
        default_format: typing.Optional[Format] = None,
        delete_characters: typing.Optional[builtins.str] = None,
        illegal_characters: typing.Optional[builtins.str] = None,
        max_length: typing.Optional[jsii.Number] = None,
        max_length_truncate_head: typing.Optional[builtins.bool] = None,
        max_part_length: typing.Optional[jsii.Number] = None,
        max_part_length_truncate_head: typing.Optional[builtins.bool] = None,
        unique_seed: typing.Any = None,
    ) -> None:
        '''
        :param default_format: When using toString(), which format should be provided? Default: - raise an error if no default specified and toString invoked
        :param delete_characters: Characters to strip from name parts. Default: '-_'
        :param illegal_characters: Characters which will cause an error if included in a name part tested AFTER deleteCharacters. Default: '!
        :param max_length: How long can the name be? Default: - no limit
        :param max_length_truncate_head: If the name exceeds maxLength, should I snip the head or the tail? Default: false
        :param max_part_length: How long can a part of the name be? Default: - no limit
        :param max_part_length_truncate_head: If the part exceeds maxPartLength, should I snip the head or the tail? Default: false
        :param unique_seed: Include a uniquifying suffix? If so, this is the seed for that suffix. Default: - do not include a uniquifier
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if default_format is not None:
            self._values["default_format"] = default_format
        if delete_characters is not None:
            self._values["delete_characters"] = delete_characters
        if illegal_characters is not None:
            self._values["illegal_characters"] = illegal_characters
        if max_length is not None:
            self._values["max_length"] = max_length
        if max_length_truncate_head is not None:
            self._values["max_length_truncate_head"] = max_length_truncate_head
        if max_part_length is not None:
            self._values["max_part_length"] = max_part_length
        if max_part_length_truncate_head is not None:
            self._values["max_part_length_truncate_head"] = max_part_length_truncate_head
        if unique_seed is not None:
            self._values["unique_seed"] = unique_seed

    @builtins.property
    def default_format(self) -> typing.Optional[Format]:
        '''When using toString(), which format should be provided?

        :default: - raise an error if no default specified and toString invoked
        '''
        result = self._values.get("default_format")
        return typing.cast(typing.Optional[Format], result)

    @builtins.property
    def delete_characters(self) -> typing.Optional[builtins.str]:
        '''Characters to strip from name parts.

        :default: '-_'
        '''
        result = self._values.get("delete_characters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def illegal_characters(self) -> typing.Optional[builtins.str]:
        '''Characters which will cause an error if included in a name part tested AFTER deleteCharacters.

        :default: '!

        :: #$%^&*()~`"' maybe more??? needs thought. Should be DNS compliant, I think.
        :todo: implement me
        '''
        result = self._values.get("illegal_characters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        '''How long can the name be?

        :default: - no limit
        '''
        result = self._values.get("max_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_length_truncate_head(self) -> typing.Optional[builtins.bool]:
        '''If the name exceeds maxLength, should I snip the head or the tail?

        :default: false
        '''
        result = self._values.get("max_length_truncate_head")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_part_length(self) -> typing.Optional[jsii.Number]:
        '''How long can a part of the name be?

        :default: - no limit
        '''
        result = self._values.get("max_part_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_part_length_truncate_head(self) -> typing.Optional[builtins.bool]:
        '''If the part exceeds maxPartLength, should I snip the head or the tail?

        :default: false
        '''
        result = self._values.get("max_part_length_truncate_head")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def unique_seed(self) -> typing.Any:
        '''Include a uniquifying suffix?

        If so, this is the seed for that suffix.

        :default: - do not include a uniquifier
        '''
        result = self._values.get("unique_seed")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Format",
    "Namer",
    "NamerProps",
]

publication.publish()

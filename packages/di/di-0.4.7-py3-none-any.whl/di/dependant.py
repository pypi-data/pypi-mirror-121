from __future__ import annotations

import inspect
from typing import Any, Dict, Optional, cast, overload

from di._docstrings import join_docstring_from
from di._inspect import DependencyParameter, get_parameters, infer_call_from_annotation
from di.exceptions import WiringError
from di.types.dependencies import DependantProtocol
from di.types.providers import (
    AsyncGeneratorProvider,
    CallableProvider,
    CoroutineProvider,
    DependencyProvider,
    DependencyProviderType,
    DependencyType,
    GeneratorProvider,
)
from di.types.scopes import Scope

_VARIABLE_PARAMETER_KINDS = (
    inspect.Parameter.VAR_POSITIONAL,
    inspect.Parameter.VAR_KEYWORD,
)


_expected_attributes = ("call", "scope", "shared", "get_dependencies", "is_equivalent")


def _is_dependant_protocol_instance(o: object) -> bool:
    # run cheap attribute checks before running isinstance
    # isinstace is expensive since runs reflection on methods
    # to check argument types, etc.
    for attr in _expected_attributes:
        if not hasattr(o, attr):
            return False
    return isinstance(o, DependantProtocol)


class Dependant(DependantProtocol[DependencyType]):
    @overload
    def __init__(
        self,
        call: Optional[AsyncGeneratorProvider[DependencyType]] = None,
        scope: Optional[Scope] = None,
        shared: bool = True,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        call: Optional[CoroutineProvider[DependencyType]] = None,
        scope: Optional[Scope] = None,
        shared: bool = True,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        call: Optional[GeneratorProvider[DependencyType]] = None,
        scope: Optional[Scope] = None,
        shared: bool = True,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        call: Optional[CallableProvider[DependencyType]] = None,
        scope: Optional[Scope] = None,
        shared: bool = True,
    ) -> None:
        ...

    def __init__(
        self,
        call: Optional[DependencyProviderType[DependencyType]] = None,
        scope: Scope = None,
        shared: bool = True,
    ) -> None:
        self.call = call
        self.scope = scope
        self.dependencies: Optional[
            Dict[str, DependencyParameter[DependantProtocol[Any]]]
        ] = None
        self.shared = shared

    @join_docstring_from(DependantProtocol[Any].create_sub_dependant)
    def create_sub_dependant(
        self, call: DependencyProvider, scope: Scope, shared: bool
    ) -> DependantProtocol[Any]:
        return Dependant[Any](call=call, scope=scope, shared=shared)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(call={self.call}, scope={self.scope})"

    @join_docstring_from(DependantProtocol[Any].__hash__)
    def __hash__(self) -> int:
        return hash(self.call)

    @join_docstring_from(DependantProtocol[Any].__eq__)
    def __eq__(self, o: object) -> bool:
        if type(self) != type(o):
            return False
        assert isinstance(o, type(self))
        if self.shared is False or o.shared is False:
            return False
        return self.call is o.call

    @join_docstring_from(DependantProtocol[Any].is_equivalent)
    def is_equivalent(self, other: DependantProtocol[Any]) -> bool:
        return self.call is other.call and other.scope == self.scope

    @join_docstring_from(DependantProtocol[Any].get_dependencies)
    def get_dependencies(
        self,
    ) -> Dict[str, DependencyParameter[DependantProtocol[Any]]]:
        if self.dependencies is None:  # type: ignore
            self.dependencies = self.gather_dependencies()
        return self.dependencies

    @join_docstring_from(DependantProtocol[Any].gather_parameters)
    def gather_parameters(self) -> Dict[str, inspect.Parameter]:
        assert self.call is not None, "Cannot gather parameters without a bound call"
        return get_parameters(self.call)

    @join_docstring_from(DependantProtocol[Any].infer_call_from_annotation)
    def infer_call_from_annotation(
        self, param: inspect.Parameter
    ) -> DependencyProvider:
        if param.annotation is param.empty:
            raise WiringError(
                "Cannot wire a parameter with no default and no type annotation"
            )
        return infer_call_from_annotation(param)

    def gather_dependencies(
        self,
    ) -> Dict[str, DependencyParameter[DependantProtocol[Any]]]:
        """Collect this dependencies sub dependencies.

        The returned dict corresponds to keyword arguments that will be passed
        to this dependencies `call` after all sub-dependencies are themselves resolved.
        """
        assert (
            self.call is not None
        ), "Container should have assigned call; this is a bug!"
        res: Dict[str, DependencyParameter[DependantProtocol[Any]]] = {}
        for param_name, param in self.gather_parameters().items():
            if param.kind in _VARIABLE_PARAMETER_KINDS:
                raise WiringError(
                    "Dependencies may not use variable positional or keyword arguments"
                )
            if _is_dependant_protocol_instance(param.default):
                sub_dependant = cast(DependantProtocol[Any], param.default)
                if sub_dependant.call is None:
                    sub_dependant.call = sub_dependant.infer_call_from_annotation(param)
            elif param.default is param.empty:
                sub_dependant = self.create_sub_dependant(
                    call=self.infer_call_from_annotation(param),
                    scope=self.scope,
                    shared=self.shared,
                )
            else:
                continue  # pragma: no cover
            res[param_name] = DependencyParameter(
                dependency=sub_dependant, parameter=param
            )
        return res

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail) -> None:
        super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )


class IdNotFoundException(HTTPException):
    def __init__(self, model, id: int = None) -> None:
        if id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the {model.__name__} with id {id}."
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} id not found."
        )


class AlreadyExistException(HTTPException):
    def __init__(self, model, name: str = None, value: str = None) -> None:
        if name and value:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{model.__name__} with {name}: {value} already exist"
            )
            return
        if value:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{model.__name__} with {value} already exist"
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Such an {model.__name__} already exists"
        )

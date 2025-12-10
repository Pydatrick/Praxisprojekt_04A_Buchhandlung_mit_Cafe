from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Type, Callable, Union, List, TypeVar
from pydantic import BaseModel

# Hints und Modeltypes
ModelType        = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound = BaseModel)
ReadSchemaType   = TypeVar("ReadSchemaType",   bound = BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound = BaseModel)

# Create
def create_post_handler(Model:Type[ModelType],
                        Schema:Type[CreateSchemaType],  # generische Factory Funktion, wird nicht genutzt, ist aber für die validierung wichtig
                        db_getter:Callable[[], Session]
                       ) -> Callable[...,Union[ModelType, List[ModelType]]]:
    
    def post_handler(item:Union[CreateSchemaType, List[CreateSchemaType]],
                     db:Session = Depends(db_getter)
                    ) -> Union[ModelType, List[ModelType]]:
        
        if isinstance(item, list):

            db_items = [Model(**list_element.model_dump()) for list_element in item]
            db.add_all(db_items)
            db.commit()
            for db_item in db_items:
                db.refresh(db_item)

            return db_items
        
        else:

            db_item = Model(**item.model_dump())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)

            return db_item

    return post_handler

# Read all
def create_read_all_handler(Model:Type[ModelType],
                            db_getter:Callable[[], Session]
                           ) -> Callable[..., List[ModelType]]:
    
    def read_all_handler(skip:int,
                         limit:int,
                         db:Session = Depends(db_getter)
                        ) -> List[ModelType]:
        
        query = db.query(Model)
        
        if skip is not None:
            query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    return read_all_handler

# Read one
def create_read_one_handler(Model:Type[ModelType],
                            db_getter:Callable[[], Session]
                           ) -> Callable[..., ModelType]:
    
    def read_one_handler(item_id:int, 
                         db: Session = Depends(db_getter)
                        ) -> ModelType:
        
        item = db.query(Model).filter(Model.id == item_id).first()
        if not item:

            raise HTTPException(status_code = 404, 
                                detail = f"{Model.__name__} with id {item_id} not found"
                               )
        
        return item
    
    return read_one_handler

# Update
def create_update_handler(Model:Type[ModelType],
                          Schema:Type[UpdateSchemaType],
                          db_getter:Callable[[], Session]
                         ) -> Callable[..., ModelType]:

    def update_handler(item_id:int,
                       update_data:UpdateSchemaType, 
                       db:Session = Depends(db_getter)
                       ) -> ModelType:
        
        item = db.query(Model).filter(Model.id == item_id).first()
        if not item:
            raise HTTPException(status_code = 404, detail = f"{Model.__name__} with id {item_id} not found")
        for key, value in update_data.model_dump(exclude_unset = True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    
    return update_handler

# Delete
def create_delete_handler(Model:Type[ModelType], 
                          db_getter:Callable[[], Session]
                         ) -> Callable[..., None]:
    
    def delete_handler(item_id:int, 
                       db:Session = Depends(db_getter)
                      ) -> None:

        item = db.query(Model).filter(Model.id == item_id).first()
        if not item:
            raise HTTPException(status_code = 404, detail = f"{Model.__name__} with id {item_id} not found")
        db.delete(item)
        db.commit()

        return None
    
    return delete_handler

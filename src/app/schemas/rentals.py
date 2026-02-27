from pydantic import BaseModel, Field, field_validator, model_validator

class RentalOutcome(BaseModel):
    bike_id: int
    user_id: int
    battery_level: float = Field(ge=0, le=100)

    @field_validator(battery_level)
    @classmethod
    def battery_must_be_sufficient(cls, value):
        if value < 20:
            raise ValueError(
                "Battery level must be at least 20% to complete a rental"
            )
        return value
    
class RentalProcessing(BaseModel):
    bike_id: int
    user_id: int
    battery_level: float = Field (ge= 0, le=100)

    @model_validator(mode="after")
    def reject_low_battery_rental(self):
        if self.battery_level < 20:
            raise ValueError("Cannot process rental: battery is below 20%.")
        return self
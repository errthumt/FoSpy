#### Required properties

During construction of a `Ramp` object, it is required to have at least 2 of the following optional properties, with their respective units:

- `temp`
- `time`
- `rate`

If all three are provided, the last one found during reading will be discarded as redundant data, and the object is [dispatched](#dispatching-subclasses) to a `Ramp` subclass with a "retrieval" method for calculating the missing property (e.g., `get_temp()`, `get_time()`, or `get_rate()`) When working with `Ramp` objects in the FoSpy framework, it is best practice to always use the "retrieval" methods. For subclasses that *do* have the desired property, retrieval methods default to returning it directly.


<prop_table>

#### Ramp Method Subclasses

The following subclasses are dispatched based on the redundant parameter (see [Required Properties](#ramp) above) and override the retrieval method to calculate the missing parameter instead of getting it from attributes:

- `RampNoRate`: overrides [`get_rate()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_rate)
- `RampNoTemp`: overrides [`get_temp()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_temp)
- `RampNoTime`: overrides [`get_time()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_time)

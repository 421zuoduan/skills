# Scientific figure workflow

## Data and provenance

Start from the current source table or run summary. Record the data source, version, condition, model, split, sample or seed aggregation, metric definition, and uncertainty definition in the script or a short README. Keep all methods in a comparison on the same data and evaluation rule. If a value, uncertainty, denominator, or significance test is not reported, do not invent it.

## Design decisions

Define the figure's conclusion and evidence unit before choosing a chart type. Prefer a simple panel when composition adds no information. Use consistent colors, markers, line styles, legend order, metric names, and units across companion figures. Remove decorative titles, redundant labels, seed annotations, unnecessary connecting lines, and legend details that do not support the intended comparison.

Make encodings honest and legible. Draw connecting elements behind data markers when both are needed. Use axis ranges that reveal the relevant variation while keeping ticks visible and comparisons fair; never alter the data or use hidden inconsistent scales to exaggerate an effect. If a truncated or local range is necessary, make it explicit in the figure or caption.

## Layout and typography

Inspect the rendered figure after each meaningful revision. Check physical width and height in the intended document placement, panel alignment, centered labels, legend position, whitespace, marker size, line z-order, label rotation, and text clipping. Match the dimensions of figures that will appear side by side. Enlarge text until it is readable at document scale, then reduce it if labels or legends exceed the canvas.

## Reproducibility and delivery

Preserve the original plotting script when creating a variant; use a clear name for the new version. Keep source data, transformation logic, and visual choices inspectable. Export the formats required by the target venue, normally an editable vector format and a raster preview. Run the script, check numerical invariants, inspect the rasterized or rendered output, and verify that vector text remains editable and no element is clipped. Do not change manuscript references implicitly when replacing a paper-facing image.

## Final figure checklist

- The displayed values match the source table after the stated rounding.
- Error bars or bands use the reported uncertainty and are labeled correctly.
- Colors and markers identify methods consistently.
- Axes, units, legends, and captions agree.
- The visual hierarchy makes the intended comparison clear without extra decoration.
- The exported figure remains readable at the size used in the manuscript.

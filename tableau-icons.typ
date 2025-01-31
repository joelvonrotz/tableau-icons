
#let PATH_ICONS = "./icons/"
#let DEFAULT_BASELINE = 15%

/* -------------------------------------------------------------------------- */
/*                              General Functions                             */
/* -------------------------------------------------------------------------- */


/// The base function used for the other functions to draw icons from Tabler.io
///
/// - body (str): icon name
/// - fill (color): color of the icon
/// - icon_type (str): style type of the icon (either "filled" or "outline") 
/// - width (length): width of the icon (icon is contained)
/// - height (length): height of the icon (icon is contained)
/// -> 
#let icon(body, fill: rgb("#000000"), icon_type: "outline", width: 1em, height: auto) = {
  if (type(body) != str) {
    panic("'icon' not set")
  }
  if ((icon_type != "filled") and (icon_type != "outline")) {
    panic("'icon' not set to either 'outline' or 'filled'")
  }

  let icon_path = PATH_ICONS + icon_type + "/" + body + ".svg"


  image.decode(
    read(icon_path).replace("currentColor", color.to-hex(fill)),
    width: width,
    height: height,
    fit: "contain",
    alt: body,
    format: "svg",
  )
}

/* -------------------------------------------------------------------------- */
/*                              Special Functions                             */
/* -------------------------------------------------------------------------- */


/// Renders the filled version of the given icon
///
/// - body (str): icon name
/// - fill (color): color of the icon
/// - width (length): width of the icon (icon is contained)
/// - height (length): height of the icon (icon is contained)
/// -> the desired icon with the parameters applied
#let filled(body, fill: rgb("#000000"), width: 1em, height: auto) = {
  icon(body, fill: fill, icon_type: "filled", width: width, height: height)
}

/// Renders the outlined version of the given icon
///
/// - body (str): icon name
/// - fill (color): color of the icon
/// - width (length): width of the icon (icon is contained)
/// - height (length): height of the icon (icon is contained)
/// -> the desired icon with the parameters applied
#let outlined(body, fill: rgb("#000000"), width: 1em, height: auto) = {
  icon(body, fill: fill, icon_type: "outline", width: width, height: height)
}

/// Renders the filled version of the given icon as an inline object
///
/// - body (str): icon name
/// - baseline (relative): the baseline position of the icon
/// - fill (color): color of the icon
/// - width (length): width of the icon (icon is contained)
/// - height (length): height of the icon (icon is contained)
/// -> the desired icon with the parameters applied
#let inline-filled(body, baseline: DEFAULT_BASELINE, fill: rgb("#000000"), width: 1em, height: auto) = {
  box(
    baseline: baseline,
    icon(body, fill: fill, icon_type: "filled", width: width, height: height),
  )
}


/// Renders the contained version of the given icon as an inline object
///
/// - body (str): icon name
/// - baseline (relative): the baseline position of the icon
/// - fill (color): color of the icon
/// - width (length): width of the icon (icon is contained)
/// - height (length): height of the icon (icon is contained)
/// -> the desired icon with the parameters applied
#let inline-outlined(body, baseline: DEFAULT_BASELINE, fill: rgb("#000000"), width: 1em, height: auto) = {
  box(
    baseline: baseline,
    icon(body, fill: fill, icon_type: "outline", width: width, height: height),
  )
}


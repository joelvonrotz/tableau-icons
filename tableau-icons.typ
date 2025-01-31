#let PATH_ICONS = "./icons/"
#let DEFAULT_BASELINE = 15%

/* -------------------------------------------------------------------------- */
/*                              General Functions                             */
/* -------------------------------------------------------------------------- */

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

#let filled(body, fill: rgb("#000000"), width: 1em, height: auto) = {
  icon(body, fill: fill, icon_type: "filled", width: width, height: height)
}

#let outlined(body, fill: rgb("#000000"), width: 1em, height: auto) = {
  icon(body, fill: fill, icon_type: "outline", width: width, height: height)
}

#let inline-filled(body, baseline: DEFAULT_BASELINE, fill: rgb("#000000"), width: 1em, height: auto) = {
  box(
    baseline: baseline,
    icon(body, fill: fill, icon_type: "filled", width: width, height: height),
  )
}

#let inline-outlined(body, baseline: DEFAULT_BASELINE, fill: rgb("#000000"), width: 1em, height: auto) = {
  box(
    baseline: baseline,
    icon(body, fill: fill, icon_type: "outline", width: width, height: height),
  )
}


#import "../lib.typ" as tableau-icons

#set page(height: 11cm, width: 21cm, margin: 5mm)
#set text(font: "Atkinson Hyperlegible Next", 10pt)

#import "thumbnail_list.typ": *
#[
  #set align(center)


  #box(clip: true, width: 100%, height: 10cm)[
    #box(
      inset: (left: -2em, top: -5em),
      width: 100%,
      height: 10cm,
      clip: true,
      rotate(
        -10deg,
        [
          #for icon in thumbnail_list {
            (
              tableau-icons.draw-icon(icon, fill: color.lighten(blue, 10%), height: 2.9em, width: 2.9em)
            )
          }
        ],
      ),
    )

    #place(
      center + horizon,
      block(
        width: 100%,
        align(center + horizon)[
          #box(
            stroke: white + 2pt,
            fill: white,
            inset: 0em,
            radius: (top: 2em, bottom: 1em),
          )[
            #box(
              stroke: black + 2pt,
              fill: white,
              inset: 2em,
              radius: 1em,
              align(center + horizon)[#text(weight: "bold", 4em, font: "Atkinson Hyperlegible Next")[tableau-icons.typ]],
            )
            #block(height: 2em, above: 0.3em)[
              #set align(center + horizon)
              #set text(1.25em)
              #grid(columns: (30%, 30%), align: (left, right))[
                *Tabler Icons Version* #tableau-icons.tabler-icons-version
              ][*Package* #tableau-icons.package-version]
            ]
          ]
        ],
      ),
    )
  ]


]
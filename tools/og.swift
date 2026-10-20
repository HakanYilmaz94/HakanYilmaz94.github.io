// Renders a 1200×630 share image (Open Graph / Twitter card).
// Usage: swift tools/og.swift <out.jpg> <plum|green> <title> <subtitle> <icon.png> [shot1 shot2 ...]
import AppKit

let a = CommandLine.arguments
let (out, theme, title, subtitle, iconPath) = (a[1], a[2], a[3], a[4], a[5])
let shots = a.dropFirst(6).compactMap { NSImage(contentsOfFile: $0) }
let W: CGFloat = 1200, H: CGFloat = 630

func color(_ h: UInt32, _ alpha: CGFloat = 1) -> NSColor {
    NSColor(srgbRed: CGFloat(h >> 16 & 255) / 255, green: CGFloat(h >> 8 & 255) / 255, blue: CGFloat(h & 255) / 255, alpha: alpha)
}
let green = theme == "green"
let top = green ? color(0x1F4D3A) : color(0x3D2660)
let bottom = green ? color(0x0A2618) : color(0x170D27)
let glows: [(UInt32, CGFloat, CGFloat, CGFloat)] = green
    ? [(0xD9B26A, 180, 120, 300), (0x6FAE8C, 1050, 560, 360), (0xE9CB8A, 900, 60, 220)]
    : [(0xCDBEEB, 160, 100, 320), (0xF6CFA8, 1080, 560, 360), (0xB9D3F2, 860, 40, 240), (0xF2B8C6, 520, 640, 260)]
let gold = color(0xF4D06F), cream = color(0xFBF4E6)

let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(W), pixelsHigh: Int(H), bitsPerSample: 8,
                           samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
let ctx = NSGraphicsContext(bitmapImageRep: rep)!
NSGraphicsContext.current = ctx
let cg = ctx.cgContext
cg.translateBy(x: 0, y: H); cg.scaleBy(x: 1, y: -1)   // top-left origin
let flipped = NSAffineTransform(); flipped.translateX(by: 0, yBy: 0)

// Background gradient + soft glows.
NSGradient(colors: [top, bottom])!.draw(in: NSRect(x: 0, y: 0, width: W, height: H), angle: 90)
for (hex, x, y, r) in glows {
    let g = NSGradient(colors: [color(hex, 0.55), color(hex, 0)])!
    g.draw(fromCenter: NSPoint(x: x, y: y), radius: 0, toCenter: NSPoint(x: x, y: y), radius: r, options: [])
}

func drawFlipped(_ image: NSImage, in r: NSRect) {
    cg.saveGState()
    cg.translateBy(x: r.minX, y: r.maxY); cg.scaleBy(x: 1, y: -1)
    image.draw(in: NSRect(x: 0, y: 0, width: r.width, height: r.height))
    cg.restoreGState()
}

// Screenshots on the right, tilted and overlapping.
let shotW: CGFloat = 250, shotH = shotW * 2868 / 1320
for (i, img) in shots.prefix(2).enumerated().reversed() {
    cg.saveGState()
    let cx: CGFloat = i == 0 ? 860 : 1040, cy: CGFloat = i == 0 ? 360 : 400
    cg.translateBy(x: cx, y: cy); cg.rotate(by: (i == 0 ? -6 : 7) * .pi / 180)
    let r = NSRect(x: -shotW / 2, y: -shotH / 2, width: shotW, height: shotH)
    cg.setShadow(offset: CGSize(width: 0, height: 24), blur: 40, color: NSColor.black.withAlphaComponent(0.45).cgColor)
    let path = NSBezierPath(roundedRect: r, xRadius: 30, yRadius: 30)
    NSColor.black.setFill(); path.fill()
    cg.setShadow(offset: .zero, blur: 0, color: nil)
    path.addClip()
    drawFlipped(img, in: r)
    cg.restoreGState()
}

// Icon, title, subtitle, domain on the left.
if let icon = NSImage(contentsOfFile: iconPath) {
    let r = NSRect(x: 80, y: 120, width: 132, height: 132)
    cg.saveGState()
    cg.setShadow(offset: CGSize(width: 0, height: 14), blur: 30, color: gold.withAlphaComponent(0.35).cgColor)
    NSBezierPath(roundedRect: r, xRadius: 30, yRadius: 30).fill()
    cg.restoreGState()
    cg.saveGState(); NSBezierPath(roundedRect: r, xRadius: 30, yRadius: 30).addClip(); drawFlipped(icon, in: r); cg.restoreGState()
}

func text(_ s: String, font: NSFont, color c: NSColor, rect: NSRect) {
    let p = NSMutableParagraphStyle(); p.lineBreakMode = .byWordWrapping; p.lineSpacing = 2
    let attr = NSAttributedString(string: s, attributes: [.font: font, .foregroundColor: c, .paragraphStyle: p])
    cg.saveGState()
    cg.translateBy(x: rect.minX, y: rect.maxY); cg.scaleBy(x: 1, y: -1)
    attr.draw(with: NSRect(x: 0, y: 0, width: rect.width, height: rect.height), options: [.usesLineFragmentOrigin])
    cg.restoreGState()
}
func serif(_ size: CGFloat, bold: Bool) -> NSFont {
    let base = NSFont.systemFont(ofSize: size, weight: bold ? .bold : .regular)
    if let d = base.fontDescriptor.withDesign(.serif) { return NSFont(descriptor: d, size: size) ?? base }
    return base
}
// NSAttributedString.draw in a flipped context draws from the top; compute rects top-down.
text(title, font: serif(72, bold: true), color: cream, rect: NSRect(x: 80, y: 280, width: 620, height: 90))
text(subtitle, font: NSFont.systemFont(ofSize: 30, weight: .regular), color: cream.withAlphaComponent(0.82),
     rect: NSRect(x: 80, y: 372, width: 580, height: 130))
text("hyapps.app", font: NSFont.systemFont(ofSize: 24, weight: .semibold), color: gold, rect: NSRect(x: 80, y: 520, width: 400, height: 36))

NSGraphicsContext.current = nil
let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.85])!
try! data.write(to: URL(fileURLWithPath: out))
print("wrote", out)

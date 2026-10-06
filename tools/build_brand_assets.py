"""Static brand sources and font-independent SVG exports. Needs fonttools[woff]."""
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
font = TTFont(ASSETS / 'fonts/geist-latin.woff2')
fonts = {}


def node(tag, attrs=None, text=None):
    e = ET.Element('{' + NS + '}' + tag, {k: str(v) for k,v in (attrs or {}).items()})
    e.text = text
    return e


def line(svg, words, x, y, size, color, weight=600):
    e = node('text', {'x':x,'y':y,'font-size':size,'font-weight':weight,'font-family':'Geist','fill':color}, words)
    svg.append(e)


def logo(svg, dark, x, y, width):
    original=ET.parse(ASSETS/'brand'/('logo-on-dark.svg' if dark else 'logo-on-light.svg')).getroot()
    group=node('g', {'transform':f'translate({x} {y}) scale({width/332})'})
    for child in original:
        group.append(deepcopy(child))
    svg.append(group)


def canvas(w,h,dark,title,desc):
    svg=node('svg', {'width':w,'height':h,'viewBox':f'0 0 {w} {h}','role':'img','aria-labelledby':'title desc'})
    svg.append(node('title',{'id':'title'},title))
    svg.append(node('desc',{'id':'desc'},desc))
    svg.append(node('rect', {'width':w,'height':h,'rx':24,'fill':'#09090b' if dark else '#fafafa'}))
    svg.append(node('rect', {'x':1,'y':1,'width':w-2,'height':h-2,'rx':24,'fill':'none','stroke':'#3f3f46' if dark else '#d4d4d8'}))
    return svg


def export(svg, name):
    (ASSETS/'sources').mkdir(exist_ok=True)
    ET.ElementTree(svg).write(ASSETS/'sources'/(name+'.svg'), encoding='unicode', xml_declaration=False)
    result=deepcopy(svg)
    for index, child in list(enumerate(result)):
        if child.tag != '{'+NS+'}text':
            continue
        weight=int(child.attrib['font-weight'])
        if weight not in fonts:
            fonts[weight]=instantiateVariableFont(font, {'wght':weight}, inplace=False) if 'fvar' in font else font
        f=fonts[weight]
        glyphs=f.getGlyphSet()
        cmap=f.getBestCmap()
        scale=float(child.attrib['font-size'])/f['head'].unitsPerEm
        x=float(child.attrib['x'])
        y=float(child.attrib['y'])
        pen=SVGPathPen(glyphs)
        for char in child.text:
            glyph_name=cmap.get(ord(char))
            if not glyph_name:
                raise ValueError('Missing glyph: '+char)
            glyphs[glyph_name].draw(TransformPen(pen,(scale,0,0,-scale,x,y)))
            x+=f['hmtx'][glyph_name][0]*scale
        if x > float(svg.attrib['width'])-32:
            raise ValueError(f'Text exceeds canvas: {name}: {child.text}, right={x}')
        path=node('path',{'d':pen.getCommands(),'fill':child.attrib['fill'],'aria-label':child.text})
        result.remove(child)
        result.insert(index,path)
    ET.ElementTree(result).write(ASSETS/(name+'.svg'),encoding='unicode',xml_declaration=False)


for dark in (True,False):
    theme='dark' if dark else 'light'
    fg='#fafafa' if dark else '#18181b'
    sub='#d4d4d8' if dark else '#52525b'
    cover=canvas(1200,760,dark,'Foundvia Discovery — You shipped it. Now get found.','An open-source discovery toolkit from Foundvia. Audit, fix, verify.')
    logo(cover,dark,64,56,600)
    line(cover,'Discovery',68,258,64,sub,500)
    line(cover,'You shipped it.',64,435,120,fg,650)
    line(cover,'Now get found.',64,565,120,fg,650)
    line(cover,'Audit. Fix. Verify.',68,690,64,sub,500)
    export(cover,'discovery-cover-'+theme)
    diagram=canvas(640,780,dark,'Evidence → one change → verification','Read the finding. Make one authorized change. Rerun and compare the evidence. A clear report is not proof of traffic.')
    for i,(heading,body) in enumerate([('Read the evidence','Find one real blocker.'),('Make one change','Keep the scope small.'),('Rerun and compare','Verify what changed.')]):
        y=110+i*238
        line(diagram,'0'+str(i+1),40,y,44,sub,500)
        line(diagram,heading,40,y+68,46,fg,600)
        line(diagram,body,40,y+120,38,sub,400)
        if i<2:
            diagram.append(node('path',{'d':f'M60 {y+144} v48 m-9 -9 9 9 9 -9','fill':'none','stroke':'#71717a','stroke-width':3}))
    export(diagram,'discovery-path-'+theme)

social=canvas(1280,640,True,'Foundvia Discovery','An open-source toolkit to find SaaS discovery blockers on Google and ChatGPT. Python auditor and practical guide.')
logo(social,True,64,36,440)
line(social,'Discovery',66,206,48,'#d4d4d8',500)
line(social,'You shipped it.',64,348,112,'#fafafa',650)
line(social,'Now get found.',64,468,112,'#fafafa',650)
line(social,'Google + ChatGPT discovery',68,564,42,'#d4d4d8',500)
export(social,'social-preview')
print('5 editable sources and 5 outlined static SVGs generated')

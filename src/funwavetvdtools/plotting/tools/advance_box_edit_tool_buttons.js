// Getting selected rect glyph index
// NOTE: Warning for multiple selected?
const inds = source.selected.indices
if (inds.length == 0) {
    console.warn("No box glyph selected")
    return
}
const ind = inds[0]

// Getting selected rect properties 
var x = source.data['x'][ind]
var y = source.data['y'][ind]
var w = source.data['w'][ind]
var h = source.data['h'][ind]

// Determining which button click was clicked by name attribute
const name = cb_obj.origin.properties.name._value
// Amount to move boundary by
const amount = amount_obj.value
switch(name) {
    case "NNORTH":
        console.error("Implement case name '" + name + "'." )
        break;
    case "NORTH":
        y = y + amount/2
        h = h + amount
        break;
    case "SNORTH":
        y = y - amount/2
        h = h - amount
        break;
    case "SSOUTH":
        console.error("Implement case name '" + name + "'." )
        break; 
    case "SOUTH":
        y = y - amount/2
        h = h + amount
        break; 
    case "NSOUTH":
        y = y + amount/2
        h = h - amount
        break;     
    case "EEAST":
        console.error("Implement case name '" + name + "'." )
        break; 
    case "EAST":
        x = x + amount/2
        w = w + amount
        break; 
    case "WEAST":
        x = x - amount/2
        w = w - amount
        break;  
     case "WWEST":
        console.error("Implement case name '" + name + "'." )
        break; 
    case "WEST":
        x = x - amount/2
        w = w + amount
        break; 
    case "EWEST":
        x = x + amount/2
        w = w - amount
        break;  
        
  default:
    // Figure out error handling. 
    console.error("Unexpected value for button widget name '" + name + "'." )
}

console.warn("Figure out callback to update numeric boxes.")

// Updating selected rect glyph properties
source.data['x'][ind] = x
source.data['y'][ind] = y
source.data['w'][ind] = w
source.data['h'][ind] = h
// Required for glyph changes to be update in renderer 
source.change.emit();
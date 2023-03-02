var inds = source.selected.indices
console.log(inds)
if (inds.length == 0) {
    x.value = 0
    y.value = 0
    w.value = 0
    h.value = 0
    xw.value = 0
    xe.value = 0
    yn.value = 0
    ys.value = 0
    return

}
var ind = inds[0]
var dict = source.data

x.value = source.data['x'][ind]
y.value = source.data['y'][ind]
w.value = source.data['w'][ind]
h.value = source.data['h'][ind]

xw.value = x.value - w.value/2
xe.value = x.value + w.value/2
ys.value = y.value - h.value/2
yn.value = y.value + h.value/2

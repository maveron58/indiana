export class Router extends THREE.Mesh {
  constructor(position, height=2.5, color="#239123") {
    var geometry = _generateGeometry(position, height);
    var material = _generateMaterial(color);

    super(geometry, material);
  }
}

// Theese are class private functions
function _generateGeometry(position, height) {
  var geometry = new THREE.CircleGeometry(0.10, 32);
  geometry.translate(position.x, -1 * position.y, 0.1);
  return geometry;
}

function _generateMaterial(color) {
  return new THREE.MeshBasicMaterial({
      color: color
  });
}

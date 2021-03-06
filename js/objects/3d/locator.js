export class Locator extends THREE.Mesh {
  constructor(color="#ff0000") {
    var geometry = _generateGeometry();
    var material = _generateMaterial(color);

    super(geometry, material);
  }

  setPosition(position) {
    this.position.x = position.x;
    this.position.y = -(position.z);
    this.position.z = position.y;
  }
}

// Theese are class private functions
function _generateGeometry() {
  // locator is 1.8 height
  var headGeometry = new THREE.SphereGeometry(0.2, 16, 16);
  var bodyGeometry = new THREE.CylinderGeometry(0.1, 0.3, 1.7, 36);

  headGeometry.translate(0, 1.7, 0);
  bodyGeometry.translate(0, 1.7 / 2, 0);
  headGeometry.merge(bodyGeometry);

  return headGeometry;
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
    color: color,
    emissive: color
  });
}

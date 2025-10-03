from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

latest_data = {"yaw": 0, "pitch": 0, "roll": 0}

@app.route("/data", methods=["POST"])
def receive_data():
    global latest_data
    latest_data = request.json
    return "OK"

@app.route("/get_data")
def get_data():
    return jsonify(latest_data)

# صفحه وب ساده برای نمایش سه‌بعدی
html_template = """
<!DOCTYPE html>
<html>
  <head>
    <title>Drone 3D Viewer</title>
    <style>
      body { margin: 0; overflow: hidden; }
      canvas { display: block; }
    </style>
  </head>
  <body>
    <script src="https://cdn.jsdelivr.net/npm/three@0.158.0/build/three.min.js"></script>
    <script>
      let scene = new THREE.Scene();
      let camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
      let renderer = new THREE.WebGLRenderer();
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.body.appendChild(renderer.domElement);

      // مکعب یا پهپاد
      let geometry = new THREE.BoxGeometry(1, 0.2, 2);
      let material = new THREE.MeshNormalMaterial();
      let cube = new THREE.Mesh(geometry, material);
      scene.add(cube);

      camera.position.z = 5;

      async function fetchData() {
        try {
          let res = await fetch("/get_data");
          let data = await res.json();

          let yaw   = data.yaw   * Math.PI / 180;
          let pitch = data.pitch * Math.PI / 180;
          let roll  = data.roll  * Math.PI / 180;

          cube.rotation.set(pitch, yaw, roll);
        } catch (e) {
          console.log("Error fetching data", e);
        }
      }

      function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      }
      animate();

      setInterval(fetchData, 100);
    </script>
  </body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# Cybersecurity Attack Map - Tecnológico de Monterrey

## Overview

This project is a web-based dashboard that visualizes cybersecurity attacks using an interactive world map. The interface dynamically loads external content, such as attack data and informational text, making it a useful display for monitoring global threats.

## Features

- **Cybersecurity Attack Map**: Displays attack data dynamically.
- **Customizable Map Markers**: Supports defining points (dots) to represent attack sources or targets.
- **Dynamic Content Loading**: Loads external widgets for real-time updates.
- **Dark Theme UI**: Styled with a custom font for a modern look.
- **Dockerized Deployment**: Easily serve the project using an Nginx container.

## Requirements

- **[Docker](https://docs.docker.com/get-docker/)** (for running the project)
- A modern web browser

## Quick Start (Using Docker + Nginx)

To serve the project using Docker and Nginx, run:

```sh
docker run --rm -p 8080:80 -v $(pwd):/usr/share/nginx/html:ro nginx
```

Then, open [http://localhost:8080/Pantalla_1.html](http://localhost:8080/Pantalla_1.html) in your browser.

## How It Works

### Dynamic Attack Map

The main interactive element is the **attack map**, loaded dynamically from:

```
Widgets/AttackMap/AttackMap_World_C.html
```

The map can display attack points (dots) by embedding JavaScript functions in the `AttackMap_World_C.html` file. Example:

```js
function addAttackPoint(lat, lng) {
    var point = document.createElement('div');
    point.style.position = 'absolute';
    point.style.width = '10px';
    point.style.height = '10px';
    point.style.background = 'red';
    point.style.borderRadius = '50%';
    point.style.top = lat + 'px';  // Adjust based on map scaling
    point.style.left = lng + 'px';
    document.querySelector('.map').appendChild(point);
}

// Example usage:
addAttackPoint(200, 450); // X, Y coordinates
```

### Loading the Map on Page Load

The JavaScript function below dynamically embeds the map inside the `.map` div:

```js
function loadMap(mapPath) {
    document.querySelector('.map').innerHTML =
        '<object class="map" type="text/html" data="' + mapPath + '"></object>';
}

window.onload = function () {
    loadMap('Widgets/AttackMap/AttackMap_World_C.html');
};
```

## Customizing the Attack Map

To define attack locations, modify `Widgets/AttackMap/AttackMap_World_C.html`:
1. Use `addAttackPoint(lat, lng)` with coordinates.
2. Adjust styling for better visibility.
3. Sync real-time data sources to reflect ongoing attacks.

## Troubleshooting

- If the map or widgets don't load:
  - Ensure `Widgets/` is correctly structured.
  - Run the project with Docker (`docker run ...`).
  - Check for JavaScript console errors (`F12` → Console).

## License

This project is intended for internal use at **Tecnológico de Monterrey**. Licensing terms may apply.

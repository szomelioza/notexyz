# notexyz

## General overview

The goal of **notexyz** is to deliver daily notes to an e-ink display that can be conveniently placed within constant line of sight, for example on a desk. The device acts as a quiet, always-visible reminder of tasks and notes for the current day.

The solution consists of three logical parts that form a simple pipeline: an input part responsible for creating and synchronizing notes, a processing part that converts notes into a displayable format, and an output part that renders the result on an e-ink display.

The overall flow looks as follows:
1. The user creates a daily note in Markdown format.
2. The note file is synchronized to a directory that is accessible by the API container.
3/ The device periodically requests the current daily note from the API.
4. The API converts the Markdown content into an image and returns it to the device.
5. The device receives the image and displays it on the e-ink screen.

## Technical overview

### Input part

notexyz operates on Markdown files provided by the user. These files must be accessible to the API container. In practice this means that a host directory containing daily notes is mounted into the container, either via a bind mount or via a Docker volume. The API itself does not care how the files arrive there, only that they are readable.

The process of creating and synchronizing daily notes is intentionally left to the user. A common and recommended setup uses Obsidian as the Markdown editor and Syncthing for synchronization. Obsidian provides a comfortable editing experience on multiple platforms, while Syncthing creates a peer-to-peer network that keeps files in sync across devices. This is not a strict requirement. Alternatives such as NFS, SMB, or any other mechanism that results in a directory with Markdown files on the Docker host are equally valid.

The API assumes a clear convention for identifying the daily note. By default, daily notes are expected to be named using the pattern `YYYY-MM-DD.md`, and the API selects the file matching the current date.

### Processing part

The processing part is implemented as an API distributed as a Docker container. A core requirement is access to the directory containing daily notes, which is achieved by mounting the directory into the container using Docker Compose.

The main responsibility of the API is to convert a daily note written in Markdown into an image. This design choice is intentional and closely tied to the constraints of the output device, which are explained in the next section.

The API exposes a single endpoint: `GET /api/note`. It accepts an optional query parameter `stream=true`. When this parameter is set, the generated image is returned as a binary stream suitable for direct consumption by the device. Without this parameter, the endpoint may be used for debugging or browser-based inspection.

### Output part

#### Overview

The output part is responsible for presenting the daily note on an e-ink display. A microcontroller wakes up at a fixed interval, currently once per hour, and sends a request to the API to fetch the image for the current daily note. If the request succeeds, the image is rendered on the display. The hourly refresh interval is a deliberate trade-off between keeping the content reasonably fresh and maintaining long battery life.

At first glance, the decision to transmit images instead of structured data such as JSON may seem unusual. In practice, this approach greatly simplifies the device firmware. Rendering formatted text, handling layout, and supporting custom fonts on a microcontroller is complex and memory-intensive. By performing all rendering on the server side and sending a ready-to-display image, the device logic remains simple and robust.

#### Configuration

The reference hardware setup consists of an Arduino Nano ESP32 paired with a Waveshare 4.2-inch e-ink display. The table below shows the required pin connections between the display and the microcontroller.

| E-ink | Arduino |
| ----- | ------- |
| BUSY  | D7      |
| RST   | D8      |
| DC    | D9      |
| CS    | D10     |
| CLK   | D13     |
| DIN   | D11     |
| GND   | GND     |
| VCC   | 3.3V    |

After wiring the hardware, the device firmware can be uploaded to the microcontroller. For the solution to work, a `secrets.h` file must be provided. This file contains network credentials and the API endpoint configuration, for example:

```cpp
#pragma once

// SSID of the network where the API is reachable
const char* SSID = "...";
// Password for the network
const char* PASSWD = "...";
// URL of the API endpoint returning the rendered image
const char* API_URL = ".../api/note?stream=true";
```

Once the secrets file is in place, the firmware can be compiled and uploaded to the microcontroller using the Arduino IDE or an equivalent toolchain. From that point on, the device operates autonomously, periodically fetching and displaying the current daily note.

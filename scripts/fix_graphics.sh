#!/bin/bash
cp config.txt config_backup.txt
sed -i 's/Renderer=OpenGL/Renderer=Direct3D/g' config.txt
echo "Graphics fixed! Toggle fullscreen with Alt+Enter if needed."

import os
from replays import create_app

app = create_app()
port = int(os.environ.get('PORT', 5000))
app.debug = os.environ.get('DEBUG', False)
app.run(host='0.0.0.0', port=port)

class Insight:
    def __init__(self, data: dict):
        if data is not None:
            self.insight_id: str = data.get('id')
            self.owner: str = data.get('owner')
            self.ancestor: str = data.get('ancestor')
            self.name: str = data.get('name')
            self.build: str = data.get('build')
            self.creation_time: str = data.get('creation_time')
            self.start_time: str = data.get('start_time')
            self.end_time: str = data.get('end_time')
            self.duration: int = data.get('duration')
            self.status: str = data.get('status')
            self.error: str = data.get('error')
            self.os: str = data.get('os')
            self.os_normalized: str = data.get('os_normalized')
            self.browser: str = data.get('browser')
            self.browser_normalized: str = data.get('browser_normalized')
            self.details_url: str = data.get('details_url')

    def __str__(self):
        return self.name

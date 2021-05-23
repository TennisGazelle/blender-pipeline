import json
import yaml
import yamale

CONFIG_FILE='./config.yaml'
SCHEMA_FILE='./scripts/config_schema.yaml'

def init_config():
    # validate the yaml first
    import yamale
    schema = yamale.make_schema(SCHEMA_FILE)
    # Create a Data object
    data = yamale.make_data(CONFIG_FILE)
    # Validate data against the schema. Throws a ValueError if data is invalid.
    yamale.validate(schema, data)

    # return it if it works
    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file)#, Loader=yaml.FullLoader) # fix this

    for stage in config['stages']:
        config['stages'][stage]['buffer_frames'] = parse_frames(config['stages'][stage]['buffer_frames'])

    return config

def parse_frames(frames_as_string):
    if type(frames_as_string) == int:
        return [ frames_as_string ]

    frames=[]
    frame_groups = frames_as_string.split(',')

    for group in frame_groups:
        if '-' in group:
            start_end_frames = group.split('-')
            for thisFrame in range(int(start_end_frames[0]), int(start_end_frames[1]) + 1):
                frames.append(int(thisFrame))
        else:
            frames.append(int(group))
    return frames

# just some default config validation
config = init_config()
print(json.dumps(config, indent=3))


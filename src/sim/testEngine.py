import model as m

engine = m.Engine()
internal_state = {
                'is_diesl': False,
                'fuel_used': 0,
                'battery': 100000000000000,
        }
external_state = {
                'grade': 1,
                'speed': 30,
                'acceleration': 0,
        }

new_internal_state = engine.tick_time(internal_state, external_state)
print(new_internal_state)

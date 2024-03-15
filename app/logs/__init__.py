from .utils import (
    add_named_logger
)

# Server log
server_log = add_named_logger('server')

# Crud
crud_log = add_named_logger('crud')

# API
line_provider_api_log = add_named_logger('line_provider_api')
bet_maker_api_log = add_named_logger('bet_maker_api')

# Scheduler
scheduler_log = add_named_logger('scheduler')

# RQ
process_event_log = add_named_logger('scheduler')

# ARMQ
armq_bet_maker_log = add_named_logger('armq_bet_maker')
# tests
tests_log = add_named_logger('tests')

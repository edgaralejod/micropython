class GenericStateMachine:
    """
    The GenericStateMachine class provides a mechanism to manage different
    states in a process, allowing for different state types. It keeps a
    dictionary, _state_handlers, to map each state to a corresponding handler
    function.

    Attributes:
      _state_handlers:
        A dictionary mapping each state to its corresponding handler function.

    Methods:
      add_state_handler(state, handler):
        Adds a handler function for a given state.

      handle_state(state):
        Handles a given state by calling the appropriate handler function,
        raising a ValueError if no handler is defined for the given state.
    """

    def __init__(self) -> None:
        """
        Initializes an empty dictionary to hold state handlers.
        """
        self._state_handlers = {}

    def add_state_handler(self, state, handler):
        """
        Adds a handler function for a given state.

        Parameters:
          state: The state for which the handler is being defined.
          handler: The function to handle the given state.
        """
        self._state_handlers[state] = handler

    def handle_state(self, state):
        """
        Handles a given state by calling the appropriate handler function.

        Parameters:
          state: The state to be handled.

        Raises:
          ValueError: If no handler is defined for the given state.
        """
        handler = self._state_handlers.get(state)
        if handler:
            handler()
        else:
            raise ValueError("No handler defined for state: {}".format(state))

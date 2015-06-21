import vespa.config.constraints as con

# how each actor is costrained to each other will be defined here


constraints = [
    # indicates that second should always be 10 units away from first
    # in a singular dimension
    # con.FixedDistance1D(['first', 'second'], length=10),
    #
]

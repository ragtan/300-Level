(define (domain Dungeon)

    (:requirements
        :typing
        :negative-preconditions
    )

    (:types
        swords cells
    )

    (:predicates
        ;Hero's cell location
        (at-hero ?loc - cells)
        
        ;Sword cell location
        (at-sword ?s - swords ?loc - cells)
        
        ;Indicates if a cell location has a monster
        (has-monster ?loc - cells)
        
        ;Indicates if a cell location has a trap
        (has-trap ?loc - cells)
        
        ;Indicates if a chell or sword has been destroyed
        (is-destroyed ?obj)
        
        ;connects cells
        (connected ?from ?to - cells)
        
        ;Hero's hand is free
        (arm-free)
        
        ;Hero's holding a sword
        (holding ?s - swords)
    
        ;It becomes true when a trap is disarmed
        (trap-disarmed ?loc)
        
    )

    ;Hero can move if the
    ;    - hero is at current location
    ;    - cells are connected, 
    ;    - there is no trap in current loc, and 
    ;    - destination does not have a trap/monster/has-been-destroyed
    ;Effects move the hero, and destroy the original cell. No need to destroy the sword.
    (:action move
        :parameters (?from ?to - cells)
        :precondition (and (at-hero ?from)
                        (connected ?from ?to)
                        (not (is-destroyed ?to))
                        (not (is-destroyed ?from))
                        (not (has-monster ?to))
                        (not (has-trap ?to))
                        (not (has-trap ?from))
                       )
        :effect (and (at-hero ?to)
                    (not (at-hero ?from))
                    (is-destroyed ?from)
                )
    )
    
    ;When this action is executed, the hero gets into a location with a trap if
    ;   - hero is at current location,
    ;   - current location must have trap,
    ;   - hero is not holding sword,
    ;   - there is not an active trap at hero's previous location, and
    ;   - destination does not have monster/has-been-destroyed.
    ; Effects move the hero to trap location, and destroy the original cell.
    (:action move-to-trap
        :parameters (?from ?to - cells)
        :precondition (and (at-hero ?from)
                        (not (is-destroyed ?from))
                        (has-trap ?to)
                        (arm-free)
                        (connected ?from ?to)
                        (not (is-destroyed ?to))
                        (not (has-monster ?to))
                        (not (trap-disarmed ?to))
                        (not (has-trap ?from))
        )
        :effect (and (at-hero ?to)
                        (not (at-hero ?from))
                        (is-destroyed ?from)
                )
    )

    ;When this action is executed, the hero gets into a location with a monster if
    ;   - hero is at current location,
    ;   - current location must have monster,
    ;   - hero is holding a sword,
    ;   - there is not an active trap at hero's previous location, and
    ;   - destination does not have trap/has-been-destroyed.
    ; Effects move the hero to monster location, and destroy the original cell.
    (:action move-to-monster
        :parameters (?from ?to - cells ?s - swords)
        :precondition (and (at-hero ?from)
                        (has-monster ?to)
                        (not (is-destroyed ?from))
                        (holding ?s)
                        (connected ?from ?to)
                        (not (is-destroyed ?to))
                        (not (has-trap ?to))
                        (not (has-trap ?from))
        )
        :effect (and (at-hero ?to)
                        (not (at-hero ?from))
                        (is-destroyed ?from)
                )
    )
    
    ;Hero picks a sword if he's in the same location
    ;   - hero is at current location,
    ;   - current location must have a sword, and
    ;   - hero is not already holding a sword.
    ; Effects hero picks up sword, arm is no longer free, sword is not at location.
    (:action pick-sword
        :parameters (?loc - cells ?s - swords)
        :precondition (and (arm-free)
                        (not (holding ?s))
                        (at-sword ?s ?loc)
                        (at-hero ?loc)
                      )
        :effect (and (holding ?s)    
                      (not (arm-free))
                      (not (at-sword ?s ?loc))
                )
    )
    
    ;Hero destroys his sword if
    ;   - hero is at current location,
    ;   - current location does not have trap/monster, and
    ;   - hero is holding a sword.
    ;Effects arm is now free and hero is not holding a sword.
    (:action destroy-sword
        :parameters (?loc - cells ?s - swords)
        :precondition (and (at-hero ?loc)
                            (not (has-trap ?loc))
                            (not (has-monster ?loc))
                            (holding ?s)
                            (not (is-destroyed ?loc))
                      )
        :effect (and (arm-free)
                      (not (holding ?s))
                )
    )
    
    ;Hero disarms the trap with his free arm if
    ;   - hero is at current location,
    ;   - current location has trap,
    ;   - hero's arm is free, and
    ;   - trap is not yet disarmed.
    ; Effects trap is disarmed, location no longer has active trap.
    (:action disarm-trap
        :parameters (?loc - cells)
        :precondition (and (at-hero ?loc)
                            (has-trap ?loc)
                            (arm-free)
                            (not (trap-disarmed ?loc))
                      )
        :effect (and (trap-disarmed ?loc)    
                    (not (has-trap ?loc))
                )
    )
)
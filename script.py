import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    for command in commands:
        line = command[0]
        args = command[1:]

        if line == 'sphere':
            add_sphere(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []

        elif line == 'torus':
            add_torus(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
            
        elif line == 'box':
            add_box(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
            
        elif line == 'circle':
            add_circle(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), step)

        elif line == 'hermite' or line == 'bezier':
            add_curve(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), step, line)                      
            
        elif line == 'line':
            add_edge( tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))

        elif line == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif line == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]


        elif line == 'rotate':
            theta = float(args[1]) * (math.pi / 180) 
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
                
        elif line == 'clear':
            tmp = []
            
        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, tmp )

        elif line == 'push':
            stack.append( [x[:] for x in stack[-1]] )
            
        elif line == 'pop':
            stack.pop()
            
        elif line == 'display' or line == 'save':
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])


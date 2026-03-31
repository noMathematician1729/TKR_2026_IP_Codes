def run_navigation_logic(L, M, R, curr_pos, next_pos, next_label, block_dict):
    cp = curr_pos[0]
    
    if cp == 0:
        block_dict[1], block_dict[2], block_dict[3] = R, M, L
        
        if block_dict[1] == "R2Real":
            next_pos[0], next_label[0] = 1, block_dict[1]
        elif block_dict[2] == "R2Real":
            next_pos[0], next_label[0] = 2, block_dict[2]
        elif block_dict[3] == "R2Real":
            next_pos[0], next_label[0] = 3, block_dict[3]
        elif block_dict[1] == "empty":
            next_pos[0], next_label[0] = 1, block_dict[1]
        elif block_dict[2] == "empty":
            next_pos[0], next_label[0] = 2, block_dict[2]
        elif block_dict[3] == "empty":
            next_pos[0], next_label[0] = 3, block_dict[3]
        else:
            next_pos[0], next_label[0] = 2, block_dict[2]

    elif cp == 1:
        block_dict[4], block_dict[5] = M, L
        if block_dict[4] == "R2Real":
            next_pos[0], next_label[0] = 4, block_dict[4]
        elif block_dict[5] == "R2Real":
            next_pos[0], next_label[0] = 5, block_dict[5]
        elif block_dict[4] == "Rsymbol":
            next_pos[0], next_label[0] = 2, block_dict[2]
        elif block_dict[5] == "Rsymbol":
            next_pos[0], next_label[0] = 2, block_dict[2]
        elif block_dict[4] == "empty":
            next_pos[0], next_label[0] = 4, block_dict[4]
        elif block_dict[5] == "empty":
            next_pos[0], next_label[0] = 5, block_dict[5]
        else:
            if block_dict[2] == "empty":
                next_pos[0], next_label[0] = 2, block_dict[2]
            else:
                next_pos[0], next_label[0] = 4, block_dict[4]

    elif cp == 2:
        block_dict[4], block_dict[5], block_dict[6] = R, M, L
        if block_dict[4] == "R2Real":
            next_pos[0], next_label[0] = 4, block_dict[4]
        elif block_dict[5] == "R2Real":
            next_pos[0], next_label[0] = 5, block_dict[5]
        elif block_dict[6] == "R2Real":
            next_pos[0], next_label[0] = 6, block_dict[6]
        elif block_dict[5] == "Rsymbol":
            next_pos[0], next_label[0] = 1, block_dict[1]
        elif block_dict[5] == "empty":
            next_pos[0], next_label[0] = 5, block_dict[5]
        elif block_dict[4] == "empty":
            next_pos[0], next_label[0] = 4, block_dict[4]
        elif block_dict[6] == "empty":
            next_pos[0], next_label[0] = 6, block_dict[6]
        else:
            if block_dict[1] == "empty":
                next_pos[0], next_label[0] = 1, block_dict[1]
            else:
                next_pos[0], next_label[0] = 5, block_dict[5]

    elif cp == 3:
        block_dict[5], block_dict[6] = M, R
        if block_dict[5] == "R2Real":
            next_pos[0], next_label[0] = 5, block_dict[5]
        elif block_dict[6] == "R2Real":
            next_pos[0], next_label[0] = 6, block_dict[6]
        elif block_dict[6] == "Rsymbol":
            next_pos[0], next_label[0] = 2, block_dict[2]
        elif block_dict[5] == "Rsymbol":
            next_pos[0], next_label[0] = 2, block_dict[2]
        elif block_dict[6] == "empty":
            next_pos[0], next_label[0] = 6, block_dict[6]
        elif block_dict[5] == "empty":
            next_pos[0], next_label[0] = 5, block_dict[5]
        else:
            if block_dict[2] == "empty":
                next_pos[0], next_label[0] = 2, block_dict[2]
            else:
                next_pos[0], next_label[0] = 6, block_dict[6]

    elif cp == 4:
        block_dict[7], block_dict[8] = M, L
        if block_dict[7] == "R2Real":
            next_pos[0], next_label[0] = 7, block_dict[7]
        elif block_dict[8] == "R2Real":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[7] == "Rsymbol":
            next_pos[0], next_label[0] = 5, block_dict[5]
        elif block_dict[8] == "Rsymbol":
            next_pos[0], next_label[0] = 5, block_dict[5]
        elif block_dict[7] == "empty":
            next_pos[0], next_label[0] = 7, block_dict[7]
        elif block_dict[8] == "empty":
            next_pos[0], next_label[0] = 8, block_dict[8]
        else:
            if block_dict[5] == "empty":
                next_pos[0], next_label[0] = 5, block_dict[5]
            else:
                next_pos[0], next_label[0] = 7, block_dict[7]

    elif cp == 5:
        block_dict[7], block_dict[8], block_dict[9] = R, M, L
        if block_dict[7] == "R2Real":
            next_pos[0], next_label[0] = 7, block_dict[7]
        elif block_dict[8] == "R2Real":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[9] == "R2Real":
            next_pos[0], next_label[0] = 9, block_dict[9]
        elif block_dict[8] == "Rsymbol":
            next_pos[0], next_label[0] = 4, block_dict[4]
        elif block_dict[8] == "empty":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[7] == "empty":
            next_pos[0], next_label[0] = 7, block_dict[7]
        elif block_dict[9] == "empty":
            next_pos[0], next_label[0] = 9, block_dict[9]
        else:
            if block_dict[4] == "empty":
                next_pos[0], next_label[0] = 4, block_dict[4]
            else:
                next_pos[0], next_label[0] = 8, block_dict[8]

    elif cp == 6:
        block_dict[8], block_dict[9] = M, R
        if block_dict[8] == "R2Real":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[9] == "R2Real":
            next_pos[0], next_label[0] = 9, block_dict[9]
        elif block_dict[9] == "Rsymbol":
            next_pos[0], next_label[0] = 5, block_dict[5]
        elif block_dict[8] == "Rsymbol":
            next_pos[0], next_label[0] = 5, block_dict[5]
        elif block_dict[9] == "empty":
            next_pos[0], next_label[0] = 9, block_dict[9]
        elif block_dict[8] == "empty":
            next_pos[0], next_label[0] = 8, block_dict[8]
        else:
            if block_dict[5] == "empty":
                next_pos[0], next_label[0] = 5, block_dict[5]
            else:
                next_pos[0], next_label[0] = 9, block_dict[9]

    elif cp == 7:
        block_dict[10], block_dict[11] = M, L
        if block_dict[8] == "empty":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[10] == "R2Real":
            next_pos[0], next_label[0] = 10, block_dict[10]
        elif block_dict[11] == "R2Real":
            next_pos[0], next_label[0] = 11, block_dict[11]
        elif block_dict[10] == "Rsymbol":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[11] == "Rsymbol":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[10] == "empty":
            next_pos[0], next_label[0] = 10, block_dict[10]
        elif block_dict[11] == "empty":
            next_pos[0], next_label[0] = 11, block_dict[11]
        else:
            next_pos[0], next_label[0] = 10, block_dict[10]

    elif cp == 8:
        block_dict[10], block_dict[11], block_dict[12] = R, M, L
        if block_dict[10] == "R2Real":
            next_pos[0], next_label[0] = 10, block_dict[10]
        elif block_dict[11] == "R2Real":
            next_pos[0], next_label[0] = 11, block_dict[11]
        elif block_dict[12] == "R2Real":
            next_pos[0], next_label[0] = 12, block_dict[12]
        elif block_dict[11] == "Rsymbol":
            next_pos[0], next_label[0] = 7, block_dict[7]
        elif block_dict[11] == "empty":
            next_pos[0], next_label[0] = 11, block_dict[11]
        elif block_dict[10] == "empty":
            next_pos[0], next_label[0] = 10, block_dict[10]
        elif block_dict[12] == "empty":
            next_pos[0], next_label[0] = 12, block_dict[12]
        else:
            if block_dict[7] == "empty":
                next_pos[0], next_label[0] = 7, block_dict[7]
            else:
                next_pos[0], next_label[0] = 11, block_dict[11]

    elif cp == 9:
        block_dict[11], block_dict[12] = M, R
        if block_dict[8] == "empty":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[11] == "R2Real":
            next_pos[0], next_label[0] = 11, block_dict[11]
        elif block_dict[12] == "R2Real":
            next_pos[0], next_label[0] = 12, block_dict[12]
        elif block_dict[12] == "Rsymbol":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[11] == "Rsymbol":
            next_pos[0], next_label[0] = 8, block_dict[8]
        elif block_dict[12] == "empty":
            next_pos[0], next_label[0] = 12, block_dict[12]
        elif block_dict[11] == "empty":
            next_pos[0], next_label[0] = 11, block_dict[11]
        else:
            next_pos[0], next_label[0] = 11, block_dict[11]

    elif cp in (10, 11, 12):
        next_pos[0], next_label[0] = cp, "EXIT"
    
    return next_pos, next_label, block_dict
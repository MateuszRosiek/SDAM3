def generate_new_id(list_with_all):
    new_id = 0

    if len(list_with_all) > 0:
        for a in list_with_all:
            if int(a['id']) > int(new_id):
                new_id = int(a['id'])

    else:
        new_id = 0

    return new_id + 1
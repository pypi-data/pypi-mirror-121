


class CommandTester():

    def __init(self):
        self.contains = []
        self.excludes = []


    def assert_command_output(self, command):

        self.command = command

        return self

    def contains(self, string):

        self.contains.append(string)

    def excluse(self, string):

        self.excludes.append(string)

    def get_test_output(self, user_id):

        command = self.command
        contains = self.contains
        excludes = self.excludes

        folder = "{}/".format(user_id)

        output, err = run_cmd(command, cwd=folder)
        if err:
            return {'status': 1, 'isRight': False}

        is_right = True
        tests = []
        for contain in contains:


            if not contain in output:

                is_right = False
                tests.append({
                    'isRight': False
                })

        for exclude in excludes :

            if exclude in output:

                is_right = False
                tests.append({'isRight': False})

        return {
            'output': {
                'isRight': is_right,
                'tests': tests
            }
        }

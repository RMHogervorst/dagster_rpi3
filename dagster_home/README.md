this is where the code lives.

You run the project from here with
`dagit`

dagit will pick up the workspace.yaml file, which points to work/repo.py
work/repo.py tells the system where all the jobs, ops, assets etc. are.

work contains the code,
work_dbt is the dbt project that gets executed within work.
work_tests contains tests to validate I did not screw stuff up.

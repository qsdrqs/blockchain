# A blockchain implementation use modified DPoS consensus mechanism

## Deployment
**Dependencies**: Python3

**Development Dependencies**: Python3, nodejs, npm/yarn

First run `pip install -r requirements.txt` to install Python dependencies.

Run `main.py` to start the simulation, after starting the simulation, you can access the simulation by http://127.0.0.1:5000.

***Warning:***: Only works fine on Unix-like systems. Use chrome/chromium for a better performance.

For front-end development, you can go to the `visible` folder and run `npm install` or `yarn install` to install front-end dependencies.

Then run `yarn run dev` or `npm run dev` to start the front-end server. Use `yarn run build` or `npm run build` to build the front-end.

## Contributing
1. Dependencies can be installed with `pip install -r requirements.txt`, and can be updated with `pip frozen > requirements.txt` when bring in new dependencies.
2. Finish the code by implementing the functions with 'pass' or 'TODO' (Can use global search to find them)
3. Use autopep8 to format the code (should be integrated in most of Python development tools, just open auto format in your IDEs)
4. Use `skeleton.py` when creating new files
5. Good to do: `FIXME` is some where that may have performance issues.

## Road map
- [x] transaction mechanism
- [x] multi threading support
- [x] graph algorithms and ledger spread
- [x] delegates ranking
- [x] ledger persistence
- [x] visualization

## Simulation
- [x] simulate small scale transaction (10 users in 5 x 5 grid)
- [x] simulate large scale transaction (100 users in 20 x 20 grid)

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the jupyterlab-rwth extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-rwth:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyterlab-rwth is activated!');
  }
};

export default plugin;

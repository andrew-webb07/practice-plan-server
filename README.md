# Practice Plan Server

## Features

The Practice Plan Server utilizes unmapped properties to send information along with the objects stored in the database, and custom actions to either send specific data to the client, or change any object properties. These features allow the client to request more precise data from the server, thereby minimizing the amount of extraneous data sent back to the client and reducing — if not eliminating — the need for client side data filtering.

## Set Up

### Installation

<ol>
    <li>Clone this repository and change to the directory in the terminal.</li>
</ol>
<div>
    <pre>
    git clone git@github.com/andrew-webb07/practice-plan-server.git
    <span>cd</span>practice-plan-server
    </pre>
</div>
<ol start="2">
    <li>Activate virtual environment</li>
</ol>
<div>
<pre>pipenv shell</pre>
</div>
<ol start="3">
    <li>Install dependencies</li>
</ol>
<div>
    <pre>pipenv install</pre>
</div>
<ol start="4">
<li><a href="https://pillow.readthedocs.io/en/stable/installation.html" rel="nofollow">Install Pillow</a></li>
</ol>
<ol start="5">
    <li>Run the server</li>
</ol>
<div>
    <pre>python manage.py runserver
</pre>
</div>
<ol start="6">
    <li>Finish installation by following the instructions found here:</li>
</ol>
<p>
    <a href="https://github.com/andrew-webb07/practice-plan-client" target="_blank">Client Repo</a>
</p>

#### Created by Andrew Webb

<a href="https://github.com/andrew-webb07/"><img src="https://camo.githubusercontent.com/6aea43d076c7bf00489f1b347caa33fe5c4d84a8af2983804f8702632f2669ec/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6769746875622532302d2532333132313031312e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" alt="Andrew Webb GitHub" data-canonical-src="https://img.shields.io/badge/github%20-%23121011.svg?&amp;style=for-the-badge&amp;logo=github&amp;logoColor=white" style="max-width: 100%;"></a>

<a href="https://www.linkedin.com/in/andrew-webb07/" rel="nofollow"><img src="https://camo.githubusercontent.com/8bb7c1de40aadb0d8eede2add7716932344b30235088d239831fe0e884de8f82/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c696e6b6564696e2532302d2532333030373742352e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d6c696e6b6564696e266c6f676f436f6c6f723d7768697465" alt="Andrew Webb LinkedIn" data-canonical-src="https://img.shields.io/badge/linkedin%20-%230077B5.svg?&amp;style=for-the-badge&amp;logo=linkedin&amp;logoColor=white" style="max-width: 100%;"></a>

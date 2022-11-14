export async function render() {
  // Fetching data
  const msg = createElement('p', 'Fetching data…');
  document.body.appendChild(msg);
  const runToTags = await fetch('./tags').then((response) => response.json());
  const data = await Promise.all(
    Object.entries(runToTags).flatMap(([run, tagToDescription]) =>
      Object.keys(tagToDescription).map((tag) =>
        fetch('./greetings?' + new URLSearchParams({run, tag}))
          .then((response) => response.json())
          .then((greetings) => ({
            run,
            tag,
            greetings,
          }))
      )
    )
  );

  // Style
  const style = createElement(
    'style',
    `
      iframe {
        box-shadow: 0 2px 8px 0 rgb(0, 0, 0, 0.2);
        padding: 6px;
        margin-left: 20px;
      }
      iframe:hover {
        box-shadow: 0 8px 32px 0 rgb(0, 0, 0, 0.2);
        scale: 1.005;
      }
      thead {
        border-bottom: 1px black solid;
        border-top: 2px black solid;
      }
      tbody {
        border: 2px black solid;
      }
      table {
        box-shadow: 0 2px 8px 0 rgb(0, 0, 0, 0.2);
        padding: 6px;
        margin-bottom: 5px;
        margin-left: 20px;
      }
      table:hover {
        box-shadow: 0 8px 32px 0 rgb(0, 0, 0, 0.2);
        scale: 1.005;
      }
      p {
        margin-left: 20px;
      }
      th {
        padding: 2pt 8pt;
      }
    `
  );
  style.innerText = style.textContent;
  document.head.appendChild(style);

  // Dynamic table
  const table = createElement('table', [
    createElement(
      'thead',
      createElement('tr', [
        createElement('th', 'Run'),
        createElement('th', 'Tag'),
        createElement('th', 'Greetings'),
      ])
    ),
    createElement(
      'tbody',
      data.flatMap(({run, tag, greetings}) =>
        greetings.map((guest, i) =>
          createElement('tr', [
            createElement('td', i === 0 ? run : null),
            createElement('td', i === 0 ? tag : null),
            createElement('td', guest),
          ])
        )
      )
    ),
  ]);
  msg.textContent = 'Data loaded.';
  document.body.appendChild(table);

  // Bootstrap: Adding HTML as an iframe
  const iframe1 = document.createElement("iframe");
  iframe1.src = "./NYC_mobility.html";
  iframe1.style.width = "46%";
  iframe1.style.height = "680px";

  const iframe2 = document.createElement("iframe");
  iframe2.src = "./VAE_mnist.html";
  iframe2.style.width = "46%";
  iframe2.style.height = "680px";

  document.body.appendChild(iframe1);
  document.body.appendChild(iframe2);
}

function createElement(tag, children) {
  const result = document.createElement(tag);
  if (children != null) {
    if (typeof children === 'string') {
      result.textContent = children;
    } else if (Array.isArray(children)) {
      for (const child of children) {
        result.appendChild(child);
      }
    } else {
      result.appendChild(children);
    }
  }
  return result;
}



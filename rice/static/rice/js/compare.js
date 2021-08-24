const phyBtn = document.querySelector('#btn-phy');
const chBtn = document.querySelector('#btn-ch');
const nuBtn = document.querySelector('#btn-nu');
const bioBtn = document.querySelector('#btn-bio');
const btnGroup = [phyBtn, chBtn, nuBtn, bioBtn];
const view = document.querySelector('.chart');
const selectChart = document.querySelector('#select-chart');
const selectX = document.querySelector('#select-x');
const selectY = document.querySelector('#select-y');
const st1 = document.querySelector('#select-type-1');
const st2 = document.querySelector('#select-type-2');

function resetNode(e) {
  while (e.lastElementChild) {
    e.removeChild(e.lastElementChild);
  }
}

function addClassPrm() {
  if (!this.hasAttribute('active')) {
    btnGroup.forEach((element) => {
      if (element.classList.contains('active')) {
        element.classList.remove('active');
        element.removeAttribute('active');
      }
    });
    this.setAttribute('active', '');
    this.classList.add('active');
  }
}

function current() {
  let fieldGroup;
  btnGroup.forEach((element) => {
    if (element.hasAttribute('active')) {
      fieldGroup = element.value;
    }
  });
  return fieldGroup;
}

btnGroup.forEach((element) => {
  element.addEventListener('click', addClassPrm);
});

phyBtn.addEventListener('click', async (e) => {
  await resetNode(view);
  const data = await getData('Physical');
  console.log(data);
  const attr = [];
  resetNode(selectX);
  resetNode(selectY);
  let name = data.fieldName;
  for (const [value, key] of Object.entries(name)) {
    if (!attr.includes(key)) {
      attr.push(key);
      let option1 = document.createElement('option');
      option1.text = key;
      option1.value = value;
      let option2 = document.createElement('option');
      option2.text = key;
      option2.value = value;
      selectX.add(option1);
      selectY.add(option2);
    }
  }
  changeChart(data);
});

chBtn.addEventListener('click', async (e) => {
  await resetNode(view);
  const data = await getData('Chemical');
  const attr = [];
  resetNode(selectX);
  resetNode(selectY);
  let name = data.fieldName;
  for (const [value, key] of Object.entries(name)) {
    if (!attr.includes(key)) {
      attr.push(key);
      let option1 = document.createElement('option');
      option1.text = key;
      option1.value = value;
      let option2 = document.createElement('option');
      option2.text = key;
      option2.value = value;
      selectX.add(option1);
      selectY.add(option2);
    }
  }
  changeChart(data);
});
nuBtn.addEventListener('click', async (e) => {
  await resetNode(view);
  const data = await getData('Nutrition');
  const attr = [];
  resetNode(selectX);
  resetNode(selectY);
  let name = data.fieldName;
  for (const [value, key] of Object.entries(name)) {
    if (!attr.includes(key)) {
      attr.push(key);
      let option1 = document.createElement('option');
      option1.text = key;
      option1.value = value;
      let option2 = document.createElement('option');
      option2.text = key;
      option2.value = value;
      selectX.add(option1);
      selectY.add(option2);
    }
  }
  changeChart(data);
});
bioBtn.addEventListener('click', async (e) => {
  await resetNode(view);
  const data = await getData('Bioactive');
  if (data.anonymous) {
    let h = document.createElement('h3');
    h.innerHTML = 'Please login to continue';
    h.classList.add('align-self-center', 'mx-auto', 'text-center');
    view.appendChild(h);
  } else {
    const attr = [];
    resetNode(selectX);
    resetNode(selectY);
    let name = data.fieldName;
    for (const [value, key] of Object.entries(name)) {
      if (!attr.includes(key)) {
        attr.push(key);
        let option1 = document.createElement('option');
        option1.text = key;
        option1.value = value;
        let option2 = document.createElement('option');
        option2.text = key;
        option2.value = value;
        selectX.add(option1);
        selectY.add(option2);
      }
    }
    changeChart(data);
  }
});
async function changeChart(data) {
  switch (selectChart.value) {
    case '1':
      markBarRowChart(data, selectX.value, selectY.value, st1.value, st2.value);
      break;
    case '2':
      markPointChart(data, selectX.value, selectY.value, st1.value, st2.value);
      break;
    case '3':
      markBox(data, selectX.value, selectY.value, st1.value, st2.value);
      break;
    default:
    // code block
  }
}

selectChart.addEventListener('change', async (e) => {
  await resetNode(view);
  let f = current();
  const data = await getData(f);
  changeChart(data);
});
selectX.addEventListener('change', async (e) => {
  await resetNode(view);
  let f = current();
  const data = await getData(f);
  changeChart(data);
});
selectY.addEventListener('change', async (e) => {
  await resetNode(view);
  let f = current();
  const data = await getData(f);
  changeChart(data);
});
st1.addEventListener('change', async (e) => {
  await resetNode(view);
  let f = current();
  const data = await getData(f);
  changeChart(data);
});
st2.addEventListener('change', async (e) => {
  await resetNode(view);
  let f = current();
  const data = await getData(f);
  changeChart(data);
});
const options = {
  config: {
    // Vega-Lite default configuration
  },
  init: (view) => {
    // initialize tooltip handler
    view.tooltip(new vegaTooltip.Handler().call);
  },
  view: {
    // view constructor options
    renderer: 'svg',
  },
};

// register vega and vega-lite with the API
vl.register(vega, vegaLite, options);

const markBarChart = async (data) => {
  const marks = vl
    .markBar({ tooltip: true, size: 25 })
    .data(data)
    .encode(
      vl.column().fieldN('cropSampleID'),
      vl.x().fieldN('riceCategories'),
      vl.y().fieldQ('length'),
      vl.color().fieldN('riceCategories'),
      vl.tooltip([vl.fieldQ('length'), vl.fieldN('riceCategories')])
    )
    .width(300)
    .height(Math.floor(300 / 1.75));
  view.appendChild(await marks.render());
};

const markBarRowChart = async (data, x, y, f1, f2) => {
  console.log(data.fieldName[y]);
  const marks = vl
    .markBar({ tooltip: true, size: 20 })
    .config({
      axis: {
        labelFontSize: 15,
        titleFontSize: 15,
        titlePadding: 20,
        domainWidth: 1,
      },
      view: { stroke: 'transparent' },
    })
    .data(data.data)
    .transform(
      vl
        .calculate('datum.cropSampleID+" "+datum.riceVarietiesEN ')
        .as('Rice Varietie')
    )
    .encode(
      vl.column().fieldO('Rice Varietie'),
      vl.x().type(f1).field(x).axis({ title: '' }),
      vl
        .y()
        .type(f2)
        .field(y)
        .axis({
          grid: false,
          title: `${data.fieldName[y]} ${
            data.fieldUnits[y] ? `(${data.fieldUnits[y]})` : ''
          }`,
        }),
      vl.color().fieldN('riceCategories')
      // ,vl.tooltip([vl.fieldQ(x), vl.fieldN(y), vl.fieldN('riceVarietiesEN')])
    )

    .width({ step: 50 })
    .height(Math.floor(500 / 1.75));
  view.appendChild(await marks.render());
};

const markPointChart = async (data, x, y, f1, f2) => {
  const marks = vl
    .markPoint({ tooltip: true, size: 500 })
    .config({
      axis: { labelFontSize: 15, titleFontSize: 15, titlePadding: 20 },
    })
    .data(data.data)
    .encode(
      vl
        .x()
        .type(f1)
        .field(x)
        .axis({
          title: `${data.fieldName[x]} ${
            data.fieldUnits[x] ? `(${data.fieldUnits[x]})` : ''
          }`,
        }),
      vl
        .y()
        .type(f2)
        .field(y)
        .axis({
          title: `${data.fieldName[y]} ${
            data.fieldUnits[y] ? `(${data.fieldUnits[y]})` : ''
          }`,
        }),
      vl.color().fieldN('riceCategories').title(data.fieldName.riceCategories),
      vl.shape().fieldN('cropSampleID').title(data.fieldName.cropSampleID),
      vl.tooltip([vl.fieldN('riceVarietiesEN'), vl.fieldN('riceCategories')])
    )
    .width(450)
    .height(Math.floor(450 / 1.75));
  view.appendChild(await marks.render());
};
const markBox = async (data, x, y, f1, f2) => {
  console.log(data.fieldName[y]);
  const marks = vl
    .markBoxplot({ tooltip: true, size: 25 })
    .config({
      axis: { labelFontSize: 15, titleFontSize: 15, titlePadding: 20 },
    })
    .data(data.data)
    .encode(
      vl
        .x()
        .type(f1)
        .field(x)
        .axis({
          title: data.fieldUnits[x]
            ? `${data.fieldName[x]} (${data.fieldUnits[x]})`
            : data.fieldName[x],
        }),
      vl.y().type(f2).field(y),
      vl.color().fieldN('riceCategories')
    )
    .width(450)
    .height(Math.floor(450 / 1.75));
  view.appendChild(await marks.render());
};
async function getData(fieldGroup) {
  const csid = window.location.search;
  try {
    const response = await fetch(`/get_data_comparison/${fieldGroup}${csid}`, {
      headers: {
        Accept: 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
    });
    return response.json();
  } catch (err) {
    throw new Error('Something failed');
  }
}

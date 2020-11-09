import { formatLocale } from 'd3-format';

var D3_LOCALE = formatLocale({
  decimal: ".",
  thousands: " ",
  grouping: [3],
  currency: ["R", ""],
});

function logIfUnequal(a, b) {
  if (a !== b) {
    console.error(`${a} !== ${b}`);
  }
}

function capFirst(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

class TextField {
  constructor(selector, value) {
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.$element.text(value);
  }
}

const pageData = JSON.parse(document.getElementById('page-data').textContent);

new TextField(".page-heading__title", pageData.geography.short_name);
new TextField(".profile-metric__population", D3_LOCALE.format(",")(pageData.total_population));
new TextField(".profile-metric__size", D3_LOCALE.format(",.1f")(pageData.geography.square_kms));
new TextField(".profile-metric__density", D3_LOCALE.format(",.1f")(pageData.population_density));

new TextField(".page-heading__muni-type", capFirst(pageData.geography.category_name));

const ancestors = pageData.geography.ancestors;
if (ancestors.length) {
  const geoParent1 = new TextField(".page-heading__geo-parent-1", ancestors[0].short_name);
  const url = `/profiles/${ ancestors[0].full_geoid }-${ ancestors[0].slug }`;
  geoParent1.$element.parent().attr("href", url);
}

new TextField(".page-heading__geo-parent-2", pageData.geography.province_name);

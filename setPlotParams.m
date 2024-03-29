function setPlotParams(x_leb,y_leb,y_lim)
ylabel(x_leb);
xlabel(y_leb);
ylim(y_lim);
etykiety = get(gca,'YTickLabel');
etykiety = strrep(etykiety (:),'.',',');
set(gca,'YTickLabel',etykiety);
etykiety = get(gca,'XTickLabel');
etykiety = strrep(etykiety (:),'.',',');
set(gca,'XTickLabel',etykiety);

end
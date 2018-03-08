select c.cui 'CUI' , c.str 'Name', s.sty 'SemanticType', d.DEF 'Definition' , c.SAB 'Source' from mrconso c , mrsty s , mrdef d where c.str like '%otitis%' and s.tui = 'T047' and c.cui = s.cui and c.cui = d.cui and d.def is not NULL and c.SAB = d.SAB and c.SAB = 'NCI' group by c.cui;


select c.cui 'CUI' , c.str 'Name', s.sty 'SemanticType', d.DEF 'Definition' , c.SAB 'Source' from mrconso c , mrsty s , mrdef d where s.tui = 'T184' and c.cui = s.cui and c.cui = d.cui and d.def is not NULL and c.SAB = d.SAB and c.SAB = 'NCI' group by c.cui;

select c.cui 'CUI' , c.str 'Name', s.sty 'SemanticType', d.DEF 'Definition' , c.SAB 'Source' from mrconso c , mrsty s , mrdef d where (s.tui = 'T032' or s.tui= 'T080' )and c.cui = s.cui and c.cui = d.cui and d.def is not NULL and c.SAB = d.SAB and c.SAB = 'NCI' group by c.cui;

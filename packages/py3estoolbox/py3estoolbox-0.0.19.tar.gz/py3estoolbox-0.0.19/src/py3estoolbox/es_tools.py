#!/usr/bin/python3 -W ignore
import os
import requests
import elasticsearch as es
import json
import py3toolbox     as tb
import py3mproc       as mp
from elasticsearch import helpers
from elasticsearch_dsl import Search


urllib3.disable_warnings()
warnings.filterwarnings("ignore")


class ES7_RAW():
  def __init__(self, es_url, username, password):
    self.es_url   = es_url
    self.endpoint = es_url
    self.username = username
    self.password = password
    self.indices = {}
    self.aliases = {}
    self.indices_list = []
    self.scanner = None
    self.read_only = False
    self.batch_data = [] 
    
    if self.username is not None or self.password is not None:
      self.endpoint = self.es_url.replace('//', '//' + self.username + ':' + self.password + '@' )
      
    self.get_es_info()       

  def _resolve_index_alias(self, index=None,alias=None, return_fmt="index"):
    assert index is not None or alias is not None, f"[index]={index}  and [alias]={alias} cannot be both None"
    assert index is None or alias is None, f"[index]={index}  and [alias]={alias} cannot be both set"
    assert index is not None or alias is not None, f"[index]={index}  and [alias]={alias} cannot be both None"
    assert index is None or alias is None, f"[index]={index}  and [alias]={alias} cannot be both set"
    assert return_fmt in ["index", "alias"], f"return_fmt [{return_fmt}] has to be either index or alias"
    
    resolved_index = None
    resolved_alias = None
    
    # resolve alias => index
    if index is None :  # if alias provided,resolve to index
      assert alias in self.aliases, f"alias={alias} doesn't exist"
      resolved_index = self.aliases[alias]
      if return_fmt == "index" :
        return resolved_index
      if return_fmt == "alias" :
        return alias
        
    # resolve index => alias
    if alias is None : # if index provided - resolve to alias
      assert index in self.indices, f"index={index} doesn't exist"
      for a in self.aliases.keys() :
        if self.aliases[a] == index :
          resolved_alias = a
          break
          
    if return_fmt == "index" :
      return index
    if return_fmt == "alias" :
      return resolved_alias

  
  
  def _call_es(self,method,uri,body=None, body_object_flag = True):
    
    headers={"content-type":"application/json"}
    url=self.endpoint + uri
    if body_object_flag == True: # assume body is dic obj
      body_text = tb.parse_json_text(body=body, return_fmt="text")
    else :
      body_text = str(body) # for bulk load only
    retry = 0
    while True:
      try:
        response = requests.request(method=method, url=url, data=body_text, headers=headers, timeout=10)
        result = tb.parse_json_text(response.text, return_fmt="dict")
        response.close()
        # check if no access  : {'ok': False, 'message': 'Forbidden'}
        if result == {'ok': False, 'message': 'Forbidden'}: 
          print ("Error to access ES: " + response.text)
          exit(1)
        return result
      except Exception as e:
        retry +=1
        if retry>=20: 
          print ("Max retries 20 reached")
          exit(1)
        print ("\nES timeout/connection exception, retry = " + str(retry))
        continue
    
  
  def _expand_bulk_exec_action(self,src_data):
    data = src_data.copy()
    op_type = data.pop("_op_type", "index")
    action = {op_type: {}}

    # If '_source' is a dict use it for source
    # otherwise if op_type == 'update' then
    # '_source' should be in the metadata.
    if (
        op_type == "update"
        and "_source" in data
        and not isinstance(data["_source"], Mapping)
    ): action[op_type]["_source"] = data.pop("_source")

    for key in (
      "_id",
      "_index",
      "_if_seq_no",
      "_if_primary_term",
      "_parent",
      "_percolate",
      "_retry_on_conflict",
      "_routing",
      "_timestamp",
      "_type",
      "_version",
      "_version_type",
      "if_seq_no",
      "if_primary_term",
      "parent",
      "pipeline",
      "retry_on_conflict",
      "routing",
      "version",
      "version_type",
    ):
      if key in data:
        if key in {
          "_if_seq_no",
          "_if_primary_term",
          "_parent",
          "_retry_on_conflict",
          "_routing",
          "_version",
          "_version_type",
        }:
          action[op_type][key[1:]] = data.pop(key)
        else:
          action[op_type][key] = data.pop(key)

    # no data payload for delete
    if op_type == "delete":
      return action, None

    return action, data.get("_source", data)


  def get_read_only(self, index=None, alias=None): 
    self.get_settings(index=index, alias=alias)
    return self.read_only
    
  def set_read_only(self, index=None, alias=None, read_only=False): 
    index = self._resolve_index_alias( index=index, alias=alias)
    # PUT "localhost:9200/%%x/_settings" -H "Content-Type: application/json" -d"{\"settings\": {\"index.blocks.write\": true}}"
    set_flag =  {"settings": {"index.blocks.write": read_only}}
    self._call_es(method="PUT", uri="/" + index + "/_settings", body=set_flag)
    assert self.get_read_only(index=index, alias=alias) == read_only, "Error set_read_only flag failed"

  
  def get_mappings(self, index=None, alias=None): 
    index = self._resolve_index_alias( index=index, alias=alias)
    self.mappings = self._call_es(method="GET", uri="/" + index + "/_mappings")[index]
    return  self.mappings
  
  
  
  def get_settings(self, index=None, alias=None): 
    index = self._resolve_index_alias( index=index, alias=alias)
    self.settings = self._call_es(method="GET", uri="/" + index + "/_settings")[index]
    if "blocks" in self.settings["settings"]["index"]:
      if "write" in  self.settings["settings"]["index"]["blocks"]:
        self.read_only = not self.settings["settings"]["index"]["blocks"]["write"]
    else:
      self.read_only = False
    return  self.settings
    
       
  def _chk_index_exist(self, index=None):
    return True
  

    
  def get_es_info(self):
    self.aliases = {}
    for item in self._call_es(method="GET", uri="/_cat/aliases?format=json&pretty"):
      if item["index"].startswith('.') : continue
      self.aliases[item["alias"]] =  item["index"]
      
    self.indices = {}
    for item in self._call_es(method="GET", uri="/_cat/indices?format=json&pretty"):
      if item["index"].startswith('.') : continue
      self.indices[item["index"]] = self._call_es(method="GET", uri="/"+item["index"])[item["index"]]
                                    
    return (self.indices,self.aliases) 
  
  def get_doc_count(self, index=None, alias=None):
    index = self._resolve_index_alias( index=index, alias=alias)
    return int(self._call_es(method="GET", uri="/" + index + "/_count")["count"])
  

  def create_index(self,index = None, body = None):
    result = self._call_es(method="PUT", uri="/" + index, body=body)
    assert "acknowledged" in result, f"{result}"
    assert result["acknowledged"] == True, f"{result}"
    self.get_es_info()
  
  def delete_index(self, index=None, alias=None):
    if index not in self.indices: return True
    
    index = self._resolve_index_alias(index=index, alias=alias)
    
    result = self._call_es(method="DELETE", uri="/" + index)
    assert result["acknowledged"] == True, f"{result}"
    self.get_es_info()
    return True
  
  

  
  def query_by_dsl(self, index=None, alias=None, dsl=None, mode="batch"):
    index = self._resolve_index_alias( index=index, alias=alias)
    assert mode in ["batch", "scan"], f"mode [{mode}] has to be either batch or scan"


    if mode == "batch" : 
      result_data = []
      for d in self.scan(index=index, alias=alias, dsl=dsl):
        result_data.append(d)

      return result_data
    
    if mode == "scan":
      return self.scan(index=index, alias=alias, dsl=dsl)
  
  def scan(self,index=None, alias=None, dsl=None, keep_alive="10m", size=1000):
    # init scanner
    index = self._resolve_index_alias( index=index, alias=alias)
    dsl_json = tb.parse_json_text(body=dsl, return_fmt="dict")
    
    if dsl_json is None: # assume all records
      dsl_json = {"query": {"match_all": {}}}

    pit_id = self._call_es(method="POST", uri="/" + index + "/_pit?keep_alive=" + keep_alive)["id"]
    
    dsl_json["size"] = size
    dsl_json["pit"] = { "id" : pit_id, "keep_alive": keep_alive  }
    dsl_json["sort"] = [ {"_score": {"order": "desc" }}]
    dsl_json.pop("search_after", None)      

    scanner = {
      "method"  : "POST",
      "uri"     : "/_search",
      "created" : tb.get_timestamp(),
      "size"    : size,
      "pit_id"  : pit_id,
      "dsl"     : tb.parse_json_text(body=dsl_json,return_fmt="text")
      
    }
    
    while True:
      result = self._call_es(method=scanner["method"], uri=scanner["uri"], body = scanner["dsl"])
      result_data = result["hits"]["hits"]
      if len(result_data) == 0 :
        break

      for r in result_data:
        yield r          
        
      last_data = result_data[-1]
      dsl_body =  tb.parse_json_text(body=scanner["dsl"],return_fmt="dict")
      dsl_body["search_after"] = last_data["sort"]
      scanner["dsl"] = tb.parse_json_text(body=dsl_body,return_fmt="text")

    # cleanup PIT
    delete_pit = self._call_es(method="DELETE", uri="/_pit", body = { "id" : scanner["pit_id"]} )
    assert delete_pit["succeeded"] == True, "Delete pit id failed"
    return 

  def clear_index(self, index=None, alias=None):
    self.delete_by_query(index=index, alias=alias, dsl=None)
    
  
  def delete_by_query(self, index=None, alias=None, dsl=None ):
    index = self._resolve_index_alias( index=index, alias=alias)

    if dsl is None: # assume all records
      dsl = {"query": {"match_all": {}}}    
    dsl_json = tb.parse_json_text(body=dsl, return_fmt="text")
    result = self._call_es(method="POST", uri="/" + index + "/_delete_by_query", body = dsl_json )
    self.refresh()
  


  def refresh(self):
    return self._call_es(method="POST", uri="/_refresh")
  
  
  def bulk_exec(self, bulk_data):
    body_text = ""
    for d in bulk_data:
      actions, data = self._expand_bulk_exec_action(d)
      body_text += json.dumps(actions) + "\n" + json.dumps(data)  + "\n"
    result = self._call_es(method="POST", uri="/_bulk", body = body_text, body_object_flag = False)
    self.refresh()
    return (result)




  def get_analyzer(self,index=None, alias=None):
    index = self._resolve_index_alias( index=index, alias=alias)
    settings = self.get_settings(index=index)
    analyzers   = {}
    for  a in settings['settings']['index']['analysis']['analyzer'].keys():
      analyzers[a] = {}
      analyzers[a]['filter'] = settings['settings']['index']['analysis']['analyzer'][a]['filter']
    return analyzers
  

  def analyze_text(self, index=None, alias=None, analyzer=None, filter=None, text=None):
    index = self._resolve_index_alias(index=index, alias=alias)
    assert analyzer is not None or filter is not None, "[analyzer] and [filter] cannot be both None"
    assert (analyzer is None) or (filter is None), "[analyzer] and [filter] cannot be both set"
    
    body = None
    if analyzer is not None: 
      body = '{"analyzer": "' + analyzer + '", "text":    "' + text + '" }'
      
    if body is None:  return {}
    
    tokens = []
    result = self._call_es(method="POST", uri="/" + index + "/_analyze", body = body)
    result = result["tokens"]
    for item in result:
      tokens.append(item["token"])
    return (tokens)


   
  def test_analyzers(self, index=None, alias=None, text=None):
    assert index is not None or alias is not None, "[index] and [alias] cannot be both None"
    if index is None: index = self.get_index_by_alias(alias=alias)
    
    analyze_result = {'analyzers': {}, 'filters': {} }
    filters = []
    for analyzer in  self.get_analyzer(index=index).keys():
      filter = self.get_analyzer(index=index)[analyzer]["filter"]
      filters.extend(filter)
      analyze_result['analyzers'][analyzer] = self.analyze_text(index=index,analyzer=analyzer,text=text)
    
    for filter in  list(set(filters)):
      analyze_result['filters'][filter]     = self.analyze_text(index=index,filter=filter,text=text)
    return analyze_result
  



class ES():
  def __init__(self, es_url):
    self.es_url  = es_url
    self.es_inst = es.Elasticsearch([self.es_url],scheme="https", verify_certs=False)
    self.indices = {}
    self.aliases = {}
    self.indices_list = []
    self.scanner = None
    self.batch_data = [] 
    self.get_es_info()
    self.scanner = None

  def get_es_info(self):
    self.indices  = { index_name: self.es_inst.indices.get('*')[index_name] for index_name in [ x for x in list( self.es_inst.indices.get('*').keys()) if not x.startswith('.') ]}
    self.aliases  = { index_name: self.es_inst.indices.get_alias('*')[index_name] for index_name in [ x for x in list( self.es_inst.indices.get_alias('*').keys()) if not x.startswith('.') ]}
    self.indices_list = list(self.indices.keys())
    self.indices_list.sort()
    return (self.indices, self.aliases)

  def show_info(self):
    info = []
    info.append("=" * (len(self.es_url) + 2))
    info.append(self.es_url)
    info.append('')
    for index in self.indices_list:
      alias = ','.join(self.aliases[index]['aliases'].keys())
      doc_count = self.get_doc_count(index=index)
      info.append(tb.format_str('{0:20} {1:10} {2:10}',index,alias,doc_count))
    info.append("-" * (len(self.es_url) + 2))
    return "\n".join(info)
  
  
  def _format_index_doc_id(self, index, doc_type,doc_id):
    return_str = '{0}|{1}|{2}'.format(index,doc_type,doc_id)
    return  return_str
    
  def _parse_index_doc_id(self, index_doc_id_str):
    m = re.match( r'^([^\|]+)\|([^\|]+)\|([^\|]+)$', index_doc_id_str, re.M|re.I)
    if m : return (m.group(1),m.group(2),m.group(3))
    else : return None   

  def init_scanner(self, index=None, alias=None, dsl_json=None):
    if index is None: index = self.get_index_by_alias(alias=alias)
    if dsl_json is None: # assume all records
      dsl_json = {"query": {"match_all": {}}}
    self.scanner = es.helpers.scan(self.es_inst, index=index, query=dsl_json)
 
  def get_index_by_alias(self, alias):
    result = []
    for k,v in self.aliases.items() :
      if alias in v['aliases']:
        result.append(k)
    if len(result) > 0: return  result[0]
    return None
  
  def delete_alias(self, alias, index=None) :
    if self.es_inst.indices.exists_alias(name=alias):
      if index is None : index = '*'
      self.es_inst.indices.delete_alias(index = index, name=alias)
 
  def set_alias(self, index, alias) :
    self.delete_alias(alias=alias)
    self.es_inst.indices.put_alias(index=index,      name=alias)       
    
  def get_doc_count(self, index=None, alias=None):
    if index is None: index = self.get_index_by_alias(alias=alias)
    return int(self.es_inst.count(index=index)['count'])

  def get_ids(self, index=None, alias=None):
    if index is None: index = self.get_index_by_alias(alias=alias)
    self.index_type_ids = []
    self.id_scanner = es.helpers.scan(self.es_inst, index=index, query={"stored_fields": ["_id"], "query": {"match_all": {}}})
    for doc in self.id_scanner :
      self.index_type_ids.append(self._format_index_doc_id(index,  doc['_type'] ,  doc['_id']))
    return (self.index_type_ids)
    
  def get_doc_by_id(self, doc_type, doc_id, index=None, alias=None) :
    if index is None: index = self.get_index_by_alias(alias=alias)
    doc = self.es_inst.search(index=index, doc_type=doc_type, body={"query": {"match": {"_id": doc_id}}})
    if int(doc['hits']['total']) == 0 : return None
    return (doc['hits']['hits'][0]['_source'])

  def bulk_exec(self, batch):
    helpers.bulk(self.es_inst, batch, request_timeout=120)
    
  def create_index(self, index, mapping_json):
    mapping = json.loads(mapping_json)
    if 'aliases' in mapping                            : mapping.pop('aliases', None)
    if 'creation_date' in mapping['settings']['index'] : mapping['settings']['index'].pop('creation_date', None)
    if 'provided_name' in mapping['settings']['index'] : mapping['settings']['index'].pop('provided_name', None)
    if 'uuid' in mapping['settings']['index']          : mapping['settings']['index'].pop('uuid', None)
    if 'version' in mapping['settings']['index']       : mapping['settings']['index'].pop('version', None)  
    
    self.es_inst.indices.create(index=index, body=json.dumps(mapping))
    self.get_es_info()
  
  def delete_index(self, index=None, alias=None):
    if index is None: index = self.get_index_by_alias(alias=alias)
    self.es_inst.indices.delete(index=index, ignore=[400, 404])
    self.get_es_info()

  def delete_index_data(self, index=None, alias=None):
    batch = []
    item_count = 0
    doc_count = self.get_doc_count(index=index)
   
    self.init_scanner(index=index)
    try :
      start_time = time.time()
      for item in self.scanner:
        item_count +=1
        item.pop('_score', None)
        item['_index'] = index
        item_to_delete = {'_op_type' : "delete",  "_index" : item['_index'] , "_type" : item['_type'] , "_id" : item['_id'] } 
        batch.append(item_to_delete) 
        
        if (item_count % config['es_bulk_size']) == 0:  
          self.bulk_exec(batch)
          print (tb.show_progress_bar(current=item_count, total=doc_count, start_time=start_time), sep=' ', end='', flush=True)  
          batch = []
      self.bulk_exec(batch)
    except Exception as e:
      self.util.write_file(config['command_log'], 'Failed: ' + str(e) + + "\n")
    if (doc_count > 0) :
      print (self.util.show_progress_bar(current=item_count, total=doc_count, start_time=start_time), sep=' ', end='', flush=True)  
    
    print ("\n\n")
    return    
    
  def get_analyzer(self,index=None, alias=None):
    mapping_dic = self.get_mapping(json_fmt=False, index=index, alias=alias)
    analyzers   = {}
    for  a in mapping_dic['settings']['index']['analysis']['analyzer'].keys():
      analyzers[a] = {}
      analyzers[a]['filter'] = mapping_dic['settings']['index']['analysis']['analyzer'][a]['filter']
    return analyzers
  
  
  def get_mapping(self, json_fmt=True, index=None, alias=None):
    if index is None: index = self.get_index_by_alias(alias=alias)
    mapping_dic = self.indices[index]
    if json_fmt :   mapping = json.dumps(mapping_dic, sort_keys=True, indent=2)
    else        :   mapping = mapping_dic
    return mapping

  def analyze_text(self, index=None, alias=None, analyzer=None, filter=None, text=None):
    if index is None: index = self.get_index_by_alias(alias=alias)
    url = self.es_url + '/' + index + '/_analyze'
    headers = {"Accept": "application/json"}
    
    if analyzer is not None: 
      body_data = '{"analyzer": "' + analyzer + '", "text":    "' + text + '" }'
      
    if filter is not None: 
      body_data = '{"filter": [' + json.dumps(filter) + '], "text":    "' + text + '" }'    
    response = requests.get(url,data = body_data)
    response_json = json.loads( response.text.replace("\\\"", "") )
    
    return (response_json)

    
    
    
  def test_analyzers(self, index=None, alias=None, text=None):
    if index is None: index = self.get_index_by_alias(alias=alias)
    analyze_result = {'analyzers': {}, 'filters': {} }
    filters = []
    for analyzer in  self.get_analyzer(index=index).keys():
      filter = self.get_analyzer(index=index)[analyzer]["filter"]
      filters.extend(filter)
      analyze_result['analyzers'][analyzer] = self.analyze_text(index=index,analyzer=analyzer,text=text)
    
    for filter in  list(set(filters)):
      analyze_result['filters'][filter]      = self.analyze_text(index=index,filter=filter,text=text)

    return analyze_result
  
  def query_by_dsl(self, doc_type, dsl_json, return_data=True, index=None, alias=None):
    if index is None: index = self.get_index_by_alias(alias=alias)
    if return_data == True :
      result = []
      result_page = self.es_inst.search(index=index, doc_type=doc_type, scroll = '5m', size=1000, body=dsl_json)
      scroll_id = result_page['_scroll_id']
      scroll_size = result_page['hits']['total']
      while (scroll_size > 0):
        result.extend(result_page['hits']['hits'])
        result_page = self.es_inst.scroll(scroll_id = scroll_id, scroll = '5m')
        scroll_id = result_page['_scroll_id']
        scroll_size = len(result_page['hits']['hits'])
      return (result)  
    else:
      result_page = self.es_inst.search(index=index, doc_type=doc_type, scroll = '5m', size=0, body=dsl_json) 
      return result_page['hits']['total']
  

  def update_index_refresh (self,  index=None, alias=None, refresh_interval_value='null') :
    if index is None: index = self.get_index_by_alias(alias=alias)
    put = self.es_inst.indices.put_settings(
        index=index,
        body='{"index": {"refresh_interval":' + refresh_interval_value + '}}',
        ignore_unavailable=True
    )

 
if __name__ == "__main__": 
  es = ES('https://vpc-tafe-search-sit-3imqbyeqvu4z7ztq5t4ndtesoy.ap-southeast-2.es.amazonaws.com')
  print (es.test_analyzers(alias='products',text='case management'))

  
  pass  
import unittest, pickle
import zelfratz

class test_zelfratz(unittest.TestCase):

    def test_create_api_request(self):
        zelfratz.key = '666'
        target = "http://api.digital-tunes.net/releases/by_artist/pyro?key=666"
        result = zelfratz.create_api_request(zelfratz.ARTIST,'pyro')
        self.assertEqual(target,result,msg="test_create_api_request failed with ARTIST")

        target = "http://api.digital-tunes.net/releases/by_label/digital_venom?key=666"
        result = zelfratz.create_api_request(zelfratz.LABEL,'digital_venom')
        self.assertEqual(target,result,msg="test_create_api_request failed with LABEL")

    def test_read_funcs(self):
        target = '0000000000'
        result = zelfratz.read_key_from_file('test_key')
        self.assertEqual(target,result,msg="read_key_from_file_failed")

        target = "pyro"
        result = zelfratz.read_key_from_file('test_artists')
        self.assertEqual(target,result,msg="read_list_from_file failed for artists")

        target = "digital_venom"
        result = zelfratz.read_key_from_file('test_labels')
        self.assertEqual(target,result,msg="read_list_from_file failed for labels")

    def test_parse_xml(self):
        self.helper_test_parse_xml('pickled_releases',
                'releases_by_label.xml',zelfratz.parse_release_xml)
        self.helper_test_parse_xml('pickled_tracks',
                'tracks_by_artist.xml',zelfratz.parse_track_xml)

    def helper_test_parse_xml(self,pickled_stuff,xml_stuff,parse_func):
        file = open(pickled_stuff)
        target = pickle.loads(pickle.load(file))
        file.close()
        file = open(xml_stuff)
        result = parse_func(file.read())
        file.close()
        self.assertEqual(target,result,msg=parse_func.func_name + 'failed')

    def test_zdata(self):
        pass

    def test_check_updates(self):
        # override to avoid downloading from digital tunes
        zelfratz.get_entity_releases = zelfratz_get_entity_releases_OVERRIDE
        zelfratz.cache = zelfratz.zdata()
        zelfratz.check_updates_artists(['pyro'])
        zelfratz.check_updates_labels(['digital_venom'])

        file = open('test_cache')
        target = pickle.loads(pickle.load(file))
        file.close()
        result = zelfratz.cache
        self.assertEqual(target,result,msg="test_check_updates failed")



def zelfratz_get_entity_releases_OVERRIDE(type, entity):
    print "zelfratz_get_entity_releases_OVERRIDE successful"
    file = None
    if type == zelfratz.LABEL:
        file = open('releases_by_label.xml')
    else:
        file = open('releases_by_artist.xml')
    s = set(zelfratz.parse_release_xml(file.read()))
    file.close()
    return s

if __name__ == '__main__':
    unittest.main()


import requests
import json

class LicencePlate:
    def __init__(self):
        pass

    def _process_json(self,jObject):
        # print('Type:',type(jObject))
        l = json.dumps(jObject)
        l = l.replace("'",'"')
        l = l.replace("False",'false')
        l = l.replace("True",'true')

        obj = json.loads(l)

        output = {}
        for r in obj['results']:
            p = str(r['plate'])
            output['Plate'] = p
            v = r['vehicle']
            make = v['make']
            makes = []
            for m in make:
                if m['confidence'] > 50:
                    # print('Make:',m['name'],m['confidence'])
                    mdict = {'make':m['name'],'confidence':m['confidence']}
                    makes.append(mdict)
            output["make"] = makes

            model = v['make_model']
            models = []
            # for m in model:
            top = 2
            for i in range(len(model)):
                if top == 0:
                    break
                m = model[i]
                top -= 1
                # print('Model:',m['name'],m['confidence'])
                mdict = {'model':m['name'],'confidence':m['confidence']}
                models.append(mdict)
            output['model'] = models

            color = v['color']
            colors = []
            # for c in color:
            top = 2
            for i in range(len(color)):
                if top == 0:
                    break
                c = color[i]
                top -= 1
                # print('Color:',c['name'],c['confidence'])        
                cdict = {'color':c['name'],'confidence':c['confidence']}
                colors.append(cdict)
            output['color'] = colors
        return output
            

    def process(self,filename):
        # form HTTP request
        v = '1'
        c = 'th'
        sk = "sk_a4ea6711f742da721bc65c46"

        url = "https://api.openalpr.com/v2/recognize?recognize_vehicle=%s&country=%s&secret_key=%s"%(v,c,sk)
        # call ALPR API
        # obtain JSON result
        r = requests.post(url, files={'image': open(filename,'rb')})
        # process JSON result
        print(r.json())
        result = self._process_json(r.json())
        return result
        # return r.json()

    def translate(self,data):
        p = data['Plate']
        s = 'ทะเบียนรถคือ %s\n' % (p)
        # How many makes?
        if len(data['make']) > 1:
            s += 'ยี่ห้อที่เป็นไปได้คือ '
            for m in data['make']:
                s += m['name'] + ' '
        else:
            s += 'ยี่ห้อ %s' % (data['make'][0]['make'])

        # How many model
        if len(data['model']) > 1:
            s += '\nรุ่นที่เป็นไปได้ คือ\n'
            for m in data['model']:
                if m['confidence'] > 50:
                    s += m['model'] + '\n'
                else:
                    s += m['model'] + ' (ไม่มั่นใจ)\n'
        else:
            s += '\nรุ่น %s' % (data['model'][0]['model'])

        # How many colors
        if len(data['color']) > 0:
            if len(data['color']) > 1:
                s += '\nสีที่เป็นไปได้ คือ\n'
                for m in data['color']:
                    if m['confidence'] > 50:
                        s += m['color'] + '\n'
                    else:
                        s += m['color'] + ' (ไม่มั่นใจ)\n'
            else:
                s += '\nสี %s' % (data['color'][0]['color'])

        return s

if __name__ == '__main__':
    lp = LicencePlate()
    filename = 'car1.jpg'
    result = lp.process(filename)
    print(result)

    s = lp.translate(result)
    print(s)